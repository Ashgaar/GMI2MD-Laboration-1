import paho.mqtt.client as mqtt
import datetime

THE_BROKER = 'broker.hivemq.com'

def on_connect(client, userdata, flags, rc):
    print(f'Flags: {flags}, return code: {str(rc)}')
    client.subscribe("miol00/devices/node1/up")
    print('Subscribed to topic: miol00/devices/node1/up')
    print('Waiting for messages...')



def on_message(client, userdata, msg):
    print(f'Received topic: {msg.topic} with payload: {msg.payload}, at subscribers local time: {datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")[:-4]}')
    send_acknowledgement()
    

def send_acknowledgement():
    print(f'Sending ACK to Device: ACK_MSG_RECEIVED')
    client.publish("miol00/devices/node1/down","ACK_MSG_RECEIVED")
    print(f'Publishing to topic: miol00/devices/node1/down')
    
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print(f'Connecting to broker: {THE_BROKER}')
client.connect(THE_BROKER, port=1883, keepalive=60)
print(f'[+] Connected to: {THE_BROKER}, port: 1883')


client.loop_forever()