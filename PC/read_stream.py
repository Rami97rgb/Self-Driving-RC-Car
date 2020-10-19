import numpy as np
import cv2
import socket
import struct
import io
import time
from keras.models import load_model


from driving_functions import slide_window, predict_sign 

def run(model, conncetion, conncetion_2):

    #count the number of detections for each object
    stop_detect = 0  
    vert_detect = 0
    rouge_detect = 0
          
    print('Start collecting images...')

    try:

        #object detection loop for each image
        while True:
            
            #get image len from stream
            image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]

            #break if equal to zero (stopped streaming)
            if not image_len:
                break
            
            #read buffer
            image_stream = io.BytesIO()
            image_stream.write(connection.read(image_len))
            image_stream.seek(0)
            data = np.frombuffer(image_stream.getvalue(), dtype=np.uint8)

            #decode and resize image
            img = cv2.imdecode(data, 1)   
            img = cv2.resize(img, (640,320))
            
            #divide image into multiple windows and apply image recognition for each window
            windows = slide_window(img, x_start_stop=[380, None], y_start_stop=[70, 180], 
                                    xy_window=(32, 32), xy_overlap=(0.25, 0.25))
            for window in windows:
                
                #select window and pass it through the model
                img_cropped =  img[window[0][1]:window[1][1],window[0][0]:window[1][0],:]
                pred_num, prob = predict_sign(img_cropped, model)  

                #detected stop sign
                if pred_num == 3 and prob > 0.99: 
                    print(pred_num, "----", prob, '----', time.time())
                    stop_detect += 1

                    #to make sure it is a stop sign and not a false positive act only there is 3 consecutive detections in a 2 second window
                    if stop_detect == 1:
                        stop_first = time.time()  
                        connection_2.send(b'0')

                    elif stop_detect == 3:  
                        if time.time() - stop_first < 2:  
                            connection_2.send(b'1')  
                            print(pred_num, "----", prob, '----', time.time())
                     
                        else:
                            stop_detect = 0 
                            connection_2.send(b'0')  
                    else:
                        connection_2.send(b'0')

                #detected red light
                elif pred_num ==1 and prob > 0.99:  
                    print(pred_num, "----", prob, '----', time.time())
                    rouge_detect += 1

                    #to make sure it is a red light and not a false positive act only there is 3 consecutive detections in a 2 second window  
                    if rouge_detect == 1:
                        rouge_first = time.time()  
                        connection_2.send(b'0')

                    elif rouge_detect == 3:  
                        if time.time() - rouge_first < 2:
                            connection_2.send(b'2')  
                            print(pred_num, "----", prob, '----', time.time())

                        else:
                            rouge_detect = 0 
                            connection_2.send(b'0') 
                    else:
                        connection_2.send(b'0') 

                #detected green light
                elif pred_num ==2 and prob > 0.99:  
                    print(pred_num, "----", prob, '----', time.time())
                    vert_detect += 1

                    #to make sure it is a green light and not a false positive act only there is 3 consecutive detections in a 2 second window
                    if vert_detect == 1:
                        vert_first = time.time()  
                        connection_2.send(b'0') 

                    elif vert_detect == 3:  
                        if time.time() - vert_first < 2:  
                            connection_2.send(b'3')  
                            print(pred_num, "----", prob, '----', time.time())
                                
                        else:
                            rouge_detect = 0 
                            connection_2.send(b'0') 
                    else:
                        connection_2.send(b'0')  

                else:
                    connection_2.send(b'0')  
                
    
    finally:
        connection.close()
        connection_2.close()
        server_socket.close()
        server_socket_2.close()

if __name__ == "__main__":
    model = load_model('traffic_model.h5')  
     
    #image stream with Raspberry
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(0)
    connection = server_socket.accept()[0].makefile('rb')
    
    #signal stream with Raspberry
    server_socket_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket_2.bind(('0.0.0.0', 8001))
    server_socket_2.listen(1)
    connection_2 = server_socket_2.accept()[0]
    
    #start receiving stream and detecting obejects
    run(model, connection, connection_2)
