import  os
from tensorflow.keras.models import model_from_json
from tensorflow.keras import models
import tensorflow as tf
import numpy as np
import cv2
import time
from os.path import dirname, join

class_names = ['bird', 'book', 'butterfly', 'cattle', 
               'chicken', 'elephant', 'horse', 
               'phone', 'sheep', 'shoes', 'spider', 'squirrel', 'watch']

def pred(img):
    current_dir = dirname(__file__)
    file_path = join(current_dir, "Classify_model.h5")
    print(file_path)
    if os.path.exists(file_path):
        model = models.load_model(file_path)
        # json_string = model.to_json()
        # model = model_from_json(json_string)
    else:
        print("trained weight file isn't exist.")
    data=cv2.resize(img,dsize=(32,32))
    data=data/255.0
    data=np.reshape(data,(1,32,32,3))
    pred_arr = model.predict(data)
    prediction = np.argmax(pred_arr[0])
    return  prediction
