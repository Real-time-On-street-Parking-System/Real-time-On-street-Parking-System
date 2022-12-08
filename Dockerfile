FROM ultralytics/yolov5:latest-cpu

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt

CMD ["gunicorn", "app:app","-c","config.py"]