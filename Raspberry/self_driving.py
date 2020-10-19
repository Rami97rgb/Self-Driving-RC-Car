import io
import socket
import struct
import serial
import time
import cv2
import numpy as np
from keras.models import load_model

import imutils
from imutils.video import VideoStream
from imutils.video import FPS

#lane keeping function
def predict_driving(img, model):
    #convert image to grayscale, resize and manipulate dimension to input it to the model
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
    img = cv2.resize(img, (320,160))  
    img = np.expand_dims(img, axis=0)  
    img = np.expand_dims(img, axis=3)  
    pred = model.predict(img)

    #get the prediction with the highest probability
    pred = np.where(pred==np.max(pred))[1][0]  
    
    #if 0 go forward
    if pred == 0:
        command = b"W"
        print('Prediction: W')
    #if 1 go left
    elif pred == 1:
        command = b"Q"
        print('Prediction: Q')
    #if 2 go right
    elif pred == 2:
        command = b"E"
        print('Prediction: E')

    return command

        
#streaming function to send video stream to the PC for object detection and to get the potential detected objects
def stream(model, ser, connection, client_socket):
    #start stream
    print("[INFO] starting video stream...")
    vs = VideoStream(src=1).start()

    print('Driving...')
    print('Press Ctrl-C to end')

    try:
        
        #read stream image by image     
        while True:
            image = vs.read()
            #resize image and put in the buffer
            image = cv2.resize(image, (640,320))
            is_success, im_buf = cv2.imencode(".jpeg", image)
            stream = io.BytesIO(im_buf)  
            BUFFER_SIZE = 1024
            print('Stream 1')
            #prepare stream to send image
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            stream.seek(0)
            #send image
            connection.write(stream.read())  

            #save stream of driving
            data = np.frombuffer(stream.getvalue(), dtype=np.uint8)
            img = cv2.imdecode(data, 1)
            cv2.imwrite('driving_frames_pi/'+str(time.time())+'.jpg', img)  
    
            #get detections from PC
            is_sign = client_socket.recv(BUFFER_SIZE)

            #print the type of the detected object
            print('Sign', is_sign)
            #stop sign
            if 49 in list(is_sign):
                print('STOP!')
                ser.write(b"O")
                time.sleep(5) 
                stop_time = time.time()  
                command = predict_driving(img, model)
                ser.write(command)  

            #green light  
            elif 51 in list(is_sign):
                print('Feu vert')
                command = predict_driving(img, model)
                ser.write(command)
            
            #red light
            elif 50 in list(is_sign):
                print('Feu rouge')
                ser.write(b"O") # Stop car

            #nothing detected   
            else:
                command = predict_driving(img, model)
                ser.write(command)

            stream.seek(0)
            stream.truncate()
                
    #stop driving
    except (KeyboardInterrupt): 
        print('Stopped')
        connection.close()
        client_socket.close()
        pass


if __name__ == "__main__":

    #load model
    model = load_model('lane_keeping_model.h5')

    #prepare connection with Arduino
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()
    
    #image stream with PC
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.1.101', 8000))
    connection = client_socket.makefile('wb')

    #signal stream with PC 
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.1.101', 8001))
    
    #start sreaming and driving
    stream(model, ser, connection, client_socket)
