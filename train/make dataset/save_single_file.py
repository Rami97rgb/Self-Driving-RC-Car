import pickle
import glob
import numpy as np
import sys


#put all the pickle files for each class in the same directory as this program
def save_single_file(name):
    final_data = []
    final_labels = []
    files = glob.glob('*.p')

    #loop over the pickle files
    for new_file in files:
        with open(new_file, mode='rb') as f:
            print('Openinig:', new_file)
            data = pickle.load(f)
            X, y = data['features'], data['labels']
            print('File size:', X.shape, y.shape)
            for i in range(len(X)):
                final_data.append(X[i])
                final_labels.append(y[i])

    #assign the whole dataset images and labels into numpy arrays
    final_data = np.array(final_data)
    final_labels = np.array(final_labels)

    print('Final size:', final_data.shape, final_labels.shape)
            
    #save dataset into a pickle file
    data_dict = {'features': final_data, 'labels': final_labels}
    with open(name+'.p', 'wb') as f:
        pickle.dump(data_dict, f, protocol=pickle.HIGHEST_PROTOCOL)
    print('Saved as '+name+'.p')
      
    
if __name__ == "__main__":

    #call program with the final pickle file name
    name = sys.argv[1]
    save_single_file(name)
    print('Finished!')