from flask import Flask,request,jsonify
import os
import torch
import cv2

model = torch.hub.load('ultralytics/yolov5','yolov5l6')

app = Flask(__name__)

UPLOAD_FOLDER = 'upload_dir'

@app.route('/esp32cam', methods=['POST'])
def upload_file():
    file = request.files['filename']
    if file.filename != '':
        save_img_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(save_img_path)
        img = cv2.imread(save_img_path)[:,:,::-1]
        res = model(img)
        res.show()
        df = res.pandas().xyxy[0]

        # print(df)
        scooter_num = len(df[df['name']=='motorcycle'])
        print(scooter_num)
        return jsonify({'num':scooter_num})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=True)