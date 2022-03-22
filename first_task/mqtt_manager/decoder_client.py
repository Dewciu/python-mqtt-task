import json
import time
from paho.mqtt.client import Client
from mqtt_manager import broker
from decoder.decoder import data_decode

decoded_data = {}

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)

def on_message(client, userdata, message):
    
    received_raw_data = message.payload.decode('UTF-8')
    json_acceptable_data = received_raw_data.replace("'", "\"")
    received_raw_dict_data = json.loads(json_acceptable_data)
    data, state = data_decode(received_raw_dict_data)

    if state == 1:
        client.publish(topic='json_data', payload = str(data))
    else:
        client.publish(topic='raw_error_data', payload = str(data))

client_name = 'decoder'
client = Client(client_name) 

client.on_connect=on_connect
print("Connecting to broker ",broker)
client.connect(broker)
client.subscribe(topic='raw_data')

client.on_message = on_message
client.loop_forever()