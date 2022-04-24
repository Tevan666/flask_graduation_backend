import  os
#from tensorflow.python.keras.models import model_from_json
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

# def pred(img):
    # print(img)
    # file_path="/home/ubuntu/api_service/detect_apis/trash/Classify_model.h5"
    # if os.path.exists(file_path):
        # model = models.load_model(file_path)
        # json_string = model.to_json()
        # model = model_from_json(json_string)
    # else:
        # print("trained weight file isn't exist.")
    # data=cv2.resize(img,dsize=(32,32))
    # data=np.reshape(data,(1,32,32,3))
    # prediction=model.predict_classes(data)[0]
    # print(prediction)
    # return  prediction
    
def pred(img):
    # print(img)
    # cv2.imshow("",img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    current_dir = dirname(__file__)
    file_path = join(current_dir, "Classify_model.h5")
    if os.path.exists(file_path):
        model = models.load_model(file_path)
        # json_string = model.to_json()
        # model = model_from_json(json_string)
    else:
        print("trained weight file isn't exist.")
    data=cv2.resize(img,dsize=(32,32))
    #cv2.imwrite("%s.jpg"%(str(time.localtime( time.time() ))),img)
    data=data/255.0
    data=np.reshape(data,(1,32,32,3))
    pred_arr = model.predict(data)
    prediction = np.argmax(pred_arr[0])
    class_name = class_names[np.argmax(pred_arr[0])]
    #print(prediction,class_name)
    return  prediction
