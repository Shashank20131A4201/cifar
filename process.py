import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from keras import *
import io
from PIL import Image
import cv2
import numpy as np
from keras.models import load_model

# file_path="static/download.png"
def process_and_return(file_path):
  image = cv2.imread(file_path)
  print("Image shape:", image.shape)
  resized_image = cv2.resize(image, (32, 32))
  input_data = np.expand_dims(resized_image, axis=0)
  input_data=input_data/255.0
  model = load_model('model_cifar.h5')
  classes = ["airplane", "automobile" , "bird", "cat", "deer", "dog", "frog", "horse", "ship",  "truck"]
  predictions=model.predict(input_data)
  # print(classes[predictions.argmax()])
  return classes[predictions.argmax()]
  

# classes = ["airplane", "automobile" , "bird", "cat", "deer", "dog", "frog", "horse", "ship",  "truck"]
# print("Class of the Image : ", classes[process_and_return(file_path)])
# process_and_return(file_path)