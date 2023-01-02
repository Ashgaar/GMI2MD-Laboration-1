import random
import time
import json
import paho.mqtt.client as mqtt
import datetime


THE_BROKER = 'broker.hivemq.com'
topic = "miol00/devices/node1/up"

def connect_mqtt():
    print(f'Connectinng to broker: {THE_BROKER}')
    client = mqtt.Client()
    client.connect(THE_BROKER, port=1883)
    print(f'[+] Connected to: {THE_BROKER}, port: 1883')
    return client


def publish(client):
    counter = 0
    while True:
        time.sleep(5)
        rssi = random.randint(20,50)
        p_channel = random.randint(1,5)
        snr = random.randint(1,30)
        temp = random.randint(23,29)

        msg = {"app_id": "miol00", "dev_id": "node1", "port/channel": p_channel, "rssi": f"-{rssi}", "snr": snr, "sf": "SF7BW125", "C_F": "C", "temperature": temp, "time": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")[:-4], "message id/counter": counter}
        msg = json.dumps(msg)
        
        print(f'Sensor data: {temp}° C at time: {datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")[:-4]}')
        
        result = client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f"Publishing to topic: {topic}, JSON payload: {msg}")
        else:
            print(f"Failed to send message to topic {topic}")
        counter += 1

def on_connect(client, userdata, flags, rc):
    print(f'Flags: {flags}, return code: {str(rc)}')
    client.subscribe("miol00/devices/node1/down")
    print(f'Subscribed to topic: miol00/devices/node1/down')
    print('Sending And Waiting for messages...')
    
def on_message(client, userdata, msg):
    print(f'Recieved topic: {msg.topic} with payload: {msg.payload}, at subscribers local time: {datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")[:-4]}')

client = connect_mqtt()

client.on_connect = on_connect
client.on_message = on_message


client.loop_start()
publish(client)

