from paho.mqtt.client import Client
from mqtt_manager import broker
import time
from file_manager.file_manager import get_raw_data

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)

def on_message(client, userdata, message):
    print(message.payload.decode('UTF-8'))

client_name = 'file_manager'
client = Client(client_name) 

client.on_connect=on_connect
print("Connecting to broker ",broker)
client.connect(broker)

while True:
    
    client.loop_start()
    raw_data = get_raw_data()
    client.on_message = on_message
    time.sleep(1)
    if len(raw_data) > 0:
        for data in raw_data:
            client.publish(topic='raw_data', payload=str(data))
            print(data)
        raw_data.clear()
    client.subscribe(topic='json_data')


