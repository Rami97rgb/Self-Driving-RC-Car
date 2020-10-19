import cv2
import numpy as np

#functions for the object detection

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


