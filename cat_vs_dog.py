# -*- coding: utf-8 -*-
"""cat vs dog.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jkgYueHvFvECV7hytHs8pcAu_BsIfSCr
"""

!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/

from google.colab import drive
drive.mount('/content/drive')

!kaggle datasets download -d salader/dogs-vs-cats

import zipfile
zip_ref = zipfile.ZipFile('/content/dogs-vs-cats.zip','r')
zip_ref.extractall('/content')
zip_ref.close()

import tensorflow as tf
from tensorflow import keras
from keras import Sequential
from keras.layers import Dense,Conv2D,MaxPool2D,Flatten,BatchNormalization,Dropout

#generators
train_ds = keras.utils.image_dataset_from_directory(
    directory = '/content/train',
    labels = 'inferred',
    label_mode='int',
    batch_size=32,
    image_size=(256,256)
)

validation_ds = keras.utils.image_dataset_from_directory(
    directory = '/content/test',
    labels = 'inferred',
    label_mode='int',
    batch_size=32,
    image_size=(256,256)
)



#normalise
def process(image,label):
  image = tf.cast(image/255.0 , tf.float32)
  return image,label

  train_ds = train_ds.map(process)
  validation_ds = validation_ds.map(process)

train_ds

from keras.src.layers.pooling.max_pooling2d import MaxPooling2D
#create CNN Model

model = Sequential()

model.add(Conv2D(32,kernel_size=(3,3),padding='valid',activation='relu',input_shape=(256,256,3)))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2),strides=2,padding='valid'))

model.add(Conv2D(64,kernel_size=(3,3),padding='valid',activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2),strides=2,padding='valid'))

model.add(Conv2D(128,kernel_size=(3,3),padding='valid',activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2),strides=2,padding='valid'))

model.add(Flatten())

model.add(Dense(128,activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(64,activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(1,activation='sigmoid'))

model.summary()

model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])

history = model.fit(train_ds,epochs=10,validation_data=validation_ds)

import matplotlib.pyplot as plt

plt.plot(history.history['accuracy'],color='red',label='train')
plt.plot(history.history['val_accuracy'],color='blue',label='validation')
plt.legend()
plt.show()

plt.plot(history.history['loss'],color='red',label='train')
plt.plot(history.history['val_loss'],color='blue',label='validation')
plt.legend()
plt.show()

# ways to reduse overfiting

# adding more data
# Data Augmentaion
# L1/L2 Regularizer
# Dropout
# Batch norm
# Reduce complexity

#testing
import cv2
test_img=cv2.imread('/content/drive/MyDrive/Colab Notebooks/dog vs cat/cat3.jpg')
plt.imshow(test_img)

test_img.shape

test_img = cv2.resize(test_img,(256,256))
test_input = test_img.reshape((1,256,256,3))

result = model.predict(test_input)
result
def float_to_int(result):
  return 1 if result >= 0.5 else 0

rt = float_to_int(result)



if rt == 0:
  print('Cat')

elif rt == 1:
  print('Dog')

else:
  print('tryagain')