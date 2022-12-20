import base64
import os
import urllib.parse
from pathlib import Path
import json
import torch
import cv2
import logging
import paho.mqtt.client as mqtt
from MongoIO import MongoIO

model = torch.hub.load('ultralytics/yolov5','yolov5l6')
logging.log(logging.DEBUG,'build model success!')

UPLOAD_FOLDER = 'C:\\Users\\PoHsien\\Desktop\\College Classes\\IOT\RTSPS\\upload_dir\\real_time_image.jpg'


def on_message_picture(client, userdata, message):
    try:
        # print("Payload: ", message.payload)
        info_str = message.payload.decode('utf-8')
        info_dict = json.loads(info_str)
        print(len(info_dict['data']))

        PICTURE_FILENAME = 'real_time_image.png'
        save_img_path = Path.cwd().joinpath(PICTURE_FILENAME)
        decoded_string = urllib.parse.unquote(info_dict['data'])
        # print("Decode URL: ", type(decoded_string))
        encoded_bytes = decoded_string.encode('utf-8')
        # print("Encoded str:", encoded_bytes)
        with open(save_img_path, "wb") as binary_file:
            decoded_img_data = base64.b64decode(encoded_bytes)
            # print(decoded_img_data)
            binary_file.write(decoded_img_data)
        
        # Run Model
        img = cv2.imread(save_img_path)[:,:,::-1]
        res = model(img)
        res.show()
        df = res.pandas().xyxy[0]

        scooter_num = len(df[df['name']=='motorcycle'])
        # print("scooter_num:", scooter_num)
        mongo_io = MongoIO()
        mongo_io.insert_parking_data(info_dict['loc'], info_dict['time'], scooter_num)

    except:
        print("Error!")

def on_connect_picture(client, userdata, flags, rc):
    print("sub_rc", rc)
    if rc == 0 :
        print("subscribing")
        client.subscribe("RTSPS_PICTURE", 2)
    else:
        print("Picture topic subscriber connection failed ", rc)

mqtt_picture_client = mqtt.Client(client_id="picture_sub", clean_session=False)
mqtt_picture_client.on_connect = on_connect_picture
mqtt_picture_client.on_message = on_message_picture
mqtt_picture_client.connect("test.mosquitto.org", 1883)
mqtt_picture_client.loop_forever()


