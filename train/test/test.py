import imutils
from imutils.video import VideoStream
from imutils.video import FPS

import numpy as np
import cv2
from keras.models import load_model


#function to make a frame the size part of the image and divide it into multiple windows
def slide_window(img, x_start_stop=[None, None], y_start_stop=[None, None], 
                    xy_window=(64, 64), xy_overlap=(0.5, 0.5)):
    
    #take the whole image if the coordinates of frame are not given 
    if x_start_stop[0] == None:
        x_start_stop[0] = 0
    if x_start_stop[1] == None:
        x_start_stop[1] = img.shape[1]
    if y_start_stop[0] == None:
        y_start_stop[0] = 0
    if y_start_stop[1] == None:
        y_start_stop[1] = img.shape[0]
    
    #size of the frame
    xspan = x_start_stop[1] - x_start_stop[0]
    yspan = y_start_stop[1] - y_start_stop[0]

    #step between two windows
    nx_pix_per_step = np.int(xy_window[0]*(1 - xy_overlap[0]))
    ny_pix_per_step = np.int(xy_window[1]*(1 - xy_overlap[1]))

    #size of the part of the window in overlap
    nx_buffer = np.int(xy_window[0]*(xy_overlap[0]))
    ny_buffer = np.int(xy_window[1]*(xy_overlap[1]))

    #number of windows in the frame
    nx_windows = np.int((xspan-nx_buffer)/nx_pix_per_step) 
    ny_windows = np.int((yspan-ny_buffer)/ny_pix_per_step)

    #save the coordinates of the windows in a list
    window_list = []
    for ys in range(ny_windows):
        for xs in range(nx_windows):
            startx = xs*nx_pix_per_step + x_start_stop[0]
            endx = startx + xy_window[0]
            starty = ys*ny_pix_per_step + y_start_stop[0]
            endy = starty + xy_window[1]
            window_list.append(((startx, starty), (endx, endy)))
    return window_list

#function to normalize the pixel values of the window
def normalize(image_data, a=0.1, b=0.9):
    return a + (((image_data-np.min(image_data)) * (b - a)) / (np.max(image_data) - np.min(image_data)))

#function to predict the traffic sign
def predict_sign(img_cropped, model):
    
    #resize, normalize, and manipulate the dimensions of the image to pass it through the model
    img_cropped = cv2.resize(img_cropped, (32,32))
    img_cropped = normalize(img_cropped)
    img_cropped = np.expand_dims(img_cropped, axis=0)
    pred = model.predict(img_cropped)
    pred_num = np.where(pred==np.max(pred))[1][0]
    prob = np.max(pred)
    
    return pred_num, prob

def sign_pipeline(path_to_images, model):
    '''
    '''
    prev_pred = 0
    '''for img_name in path_to_images:'''
    while True:
        image = path_to_images.read()
        '''image = cv2.imread(img_name)'''
        image = cv2.resize(image, (640,480))
        img_2 = image.copy()
        mask, image = sign_threshold(image)
        windows = slide_window(image, x_start_stop=[450,None], y_start_stop=[70,180], #hadhi hiya 
                                        xy_window=(32, 32), xy_overlap=(0.25, 0.25))
        img_tiny = []
        img_sign = None
        for window in windows:
            #cv2.rectangle(image, window[0], window[1], (0,0,255), 4) # show all boxes
            if np.sum(mask[window[0][1]:window[1][1],window[0][0]:window[1][0]]) <= 100000:
                next
            else:
             #   cv2.rectangle(image, window[0], window[1], (0,0,255), 4) # show thresholded boxes
                img_cropped =  img_2[window[0][1]:window[1][1],window[0][0]:window[1][0],:]
                img_cropped_copy = img_cropped.copy()
                pred_num, prob = predict_sign(img_cropped, model)
                if pred_num != 0 and prob > 0.99:
                    #cv2.imwrite('test_new/'+str(time.time())+'_'+str(pred_num)+'_.jpg', image) #img_cropped_copy
                    if  prev_pred == pred_num:
                        img_tiny = img_cropped_copy      
                        img_sign = cv2.imread('traffic_sign_img/sign_'+str(pred_num)+'.jpg')
                        cv2.rectangle(image, window[0], window[1], (0,255,0), 4)
                    prev_pred = pred_num
                    
        if len(img_tiny) != 0:
            y_offset = 60; x_offset = 0
            image[y_offset:y_offset+img_sign.shape[0], x_offset:x_offset+img_sign.shape[1]] = img_sign
            y_offset = img_sign.shape[0] + 60
            image[y_offset:y_offset+img_tiny.shape[0], x_offset:x_offset+img_tiny.shape[1]] = img_tiny 
        cv2.imshow('image', image)
        key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

	# update the FPS counter
        '''cv2.waitKey(0)
        cv2.destroyAllWindows()'''
        #cv2.imwrite('test_new/'+str(time.time())+'_'+str(pred_num)+'_.jpg', image) #img_cropped_copy
    
    return 0

import imutils
from imutils.video import VideoStream
from imutils.video import FPS

from keras.models import load_model
import glob
import time
from traffic_sign_functions import sign_pipeline    

'''model = load_model('model_traffic_2_10epochs.h5')

path_name = 'traffic_sign_test/'
path = glob.glob(path_name + '*.jpg')
sign_pipeline(path, model)'''

model = load_model('model_traffic_2_20epochs.h5')
print("[INFO] starting video stream...")
vs = VideoStream(src=1).start()
sign_pipeline(vs, model)