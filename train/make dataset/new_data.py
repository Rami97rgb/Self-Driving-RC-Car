import pickle
import numpy as np
import glob
import cv2
import sys


def get_new_data(label, data_dir):

    #get the path of the trainings images
    path = glob.glob(data_dir+'/*.jpg')
    img_list = []

    #loop over the paths of all the images 
    for img_name in path:
        img = cv2.imread(img_name)
        img = cv2.resize(img, (32,32))
        img_list.append(img)

    #assign the images and their labels into numpy arrays  
    img_list = np.array(img_list)
    labels = np.zeros(len(img_list))
    labels.fill(label)
    
    #save the data into pickle file
    data_dict = {'features': img_list, 'labels': labels}
    with open(data_dir+'.p', 'wb') as file:
       pickle.dump(data_dict, file, protocol=pickle.HIGHEST_PROTOCOL)
    

if __name__ == "__main__":

    #call the program with the class number and the path of the images, repeat for each class
    label = int(sys.argv[1])
    data_dir = sys.argv[2]
    get_new_data(label, data_dir)
    print('Finished!')
