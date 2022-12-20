import paho.mqtt.client as mqtt
from MongoIO import MongoIO

def on_message_will(client, userdata, message):
    print("Will message payload: ", message.payload)
    loc, status = message.payload.decode("utf-8").split()
    status = True if status == "Connected" else False
    print(loc, status)

    mongo_io = MongoIO()
    mongo_io.set_parking_space_connection_status(loc, status)
    
def on_connect_will(client, userdata, flags, rc):
    if rc == 0:
        client.subscribe("RTSPS_WILL", 1)
    else:
        print("Will topic subscriber connection failed", rc)

mqtt_monitor_client = mqtt.Client(client_id="will_sub", clean_session=False)
mqtt_monitor_client.on_connect = on_connect_will
mqtt_monitor_client.on_message = on_message_will
mqtt_monitor_client.connect("test.mosquitto.org", 1883)
mqtt_monitor_client.loop_forever()