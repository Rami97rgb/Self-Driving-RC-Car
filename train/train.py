import pickle
import numpy as np

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.utils import np_utils

from sklearn.model_selection import train_test_split

#normalize the pixel values of the image to pass it through the model
def normalize(image_data, a=0.1, b=0.9):
    return a + (((image_data-np.min(image_data)) * (b - a)) / (np.max(image_data) - np.min(image_data)))

#training hyperparameters
batch_size = 64
nb_classes = 4  
nb_epoch = 20

#image shape
img_rows, img_cols, channels = 32, 32, 3

#load dataset
training_file = 'dataset/dataset.p'
with open(training_file, mode='rb') as f:
    data = pickle.load(f)

#split dataset into training and validation  
X, y = data['features'], data['labels']
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=42)

#normalize dataset
X_train = normalize(X_train)
X_valid = normalize(X_valid)

#convert class ids into one-hot vectors
y_train = np_utils.to_categorical(y_train, nb_classes)
y_valid = np_utils.to_categorical(y_valid, nb_classes)

#build model
model = Sequential()

model.add(Convolution2D(24, 5, 5, border_mode='valid', input_shape=(img_rows, img_cols, channels)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Convolution2D(64, 5, 5, border_mode='valid'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Convolution2D(64, 3, 3, border_mode='valid'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.5))

model.add(Flatten())
model.add(Dense(240))
model.add(Activation('relu'))
model.add(Dropout(0.5))

model.add(Dense(168))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(nb_classes))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

#train model
model.fit(X_train, y_train, batch_size=batch_size, nb_epoch=nb_epoch, validation_data=(X_valid, y_valid))

#save model 
model.save('traffic_model.h5')