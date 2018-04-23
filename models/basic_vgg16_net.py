# coding: utf-8

import keras
import os
from keras.applications.vgg16 import VGG16
import numpy as np
import cv2
from keras.layers import Input,merge, concatenate, Conv2D, MaxPooling2D, Activation, UpSampling2D,Dropout,Conv2DTranspose,add,multiply,Flatten,Dense
from keras.models import Model
import os
import glob

x_train_path = '/home/omid/teamRope/team-rope/data/train_np_90k/'

# check if the model has been saved before, load it,
if os.path.isfile('vgg16.h5') :
    print("Loading from saved model ....")
    model = Model.load('vgg16.h5')
else:
    # Load the VGG model
    vgg_conv = VGG16(weights='imagenet',  include_top=False, input_shape=(64, 64, 3))
     # freezing first layers:
     # Freeze the layers except the last 4 layers
    for layer in vgg_conv.layers[:-4]:
        layer.trainable = False

    model=vgg_conv

    # x = Dropout(0.2)( model.layers[-2].output)
    x = Flatten(name='flatten')(model.layers[-2].output)
    # x = Dropout(0.2)(x)
    x = Dense(9000, activation='relu', name='fc1')(x)
    x = Dense(9000, activation='relu', name='fc2')(x)
    x = Dense(15000, activation='softmax', name='predictions')(x)
    # x = Dense(15000, activation='softmax', name='predictions')()

    model = Model( input= model.input , output= x )

    model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])

print(model.summary())


for i in range(0, len( glob.glob( x_train_path + 'X_*.npy'))):
  print(i)

  X_train=np.load(( x_train_path + "X_train"+str(i)+".npy"))
  # X_train = X_train.astype('float32')

  y_train=np.load((  x_train_path + "y_train"+str(i)+".npy"))#.reshape(X_train.shape)
  y_train=keras.utils.to_categorical(y_train, 15000)

  model.fit([X_train], [y_train],
                    batch_size=120,
                    epochs=1,
                    validation_split=0.2,
                    shuffle=True
            )

  model.save(  'vgg16.h5' )



