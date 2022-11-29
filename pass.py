import os
import torch
import cv2
import time
import pandas as pd

model = torch.hub.load('ultralytics/yolov5','yolov5l6')
data_dir = r'D:\works\iot\Download'
pass_list = []

for filename in os.listdir(data_dir):
    file_path = os.path.join(data_dir,filename)
    img = cv2.imread(file_path)[:,:,::-1]
    res = model(img)
    df = res.pandas().xyxy[0]

    scooter_num = len(df[df['name']=='motorcycle'])
    pass_list.append({'loc':os.path.splitext(filename)[0],'time': time.ctime(os.path.getmtime(file_path)),'num':scooter_num})

df = pd.DataFrame(pass_list)
df.to_csv('results.csv')