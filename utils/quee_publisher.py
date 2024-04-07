
import random
import time
import base64
from paho.mqtt import client as mqtt_client


connected=False

broker = 'localhost'
port = 1883
topic = "hello/topic"
# Generate a Client ID with the subscribe prefix.
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'user1'
password = '123123123'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc, self):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    #client = mqtt_client.Client(client_id)
    client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    #client.loop_start ()
    #while connected!=True:
        #time.sleep (0.2)
    return client


def publish(client):
    msg_count = 1
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        if msg_count > 5:
            break

def publish_img(client, img):
    
    # todo : convert image to base64
    base64_content = base64.b64encode(img)
    result = client.publish(topic, base64_content)
        
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

def execute(img):
    client = connect_mqtt()
    client.loop_start()
    publish_img(client, img)
    client.loop_stop() 
