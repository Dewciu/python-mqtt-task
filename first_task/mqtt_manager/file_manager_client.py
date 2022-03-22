from paho.mqtt.client import Client
from mqtt_manager import broker
import json
import time
from file_manager.file_manager import FileManager

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)

def on_message(client, userdata, message):

    if message.topic == 'json_data':
        received_json_data = message.payload.decode('UTF-8')
        json_acceptable_data = received_json_data.replace("'", "\"")
        received_json_dict_data = json.loads(json_acceptable_data)
        filemanager.create_json_file(received_json_dict_data)

    elif message.topic == 'raw_error_data':

        received_raw_error_data = message.payload.decode('UTF-8')
        json_acceptable_data = received_raw_error_data.replace("'", "\"")
        received_error_data = json.loads(json_acceptable_data)
        filemanager.create_error_file(received_error_data)


client_name = 'file_manager'
client = Client(client_name) 

client.on_connect=on_connect
print("Connecting to broker ",broker)
client.connect(broker)

while True:

    client.loop_start()
    client.on_message = on_message

    client.subscribe(topic='json_data')
    client.subscribe(topic='raw_error_data')

    filemanager = FileManager()

    raw_data = filemanager.get_raw_data()

    if len(raw_data) > 0:
        for data in raw_data:
            # print(data)
            client.publish(topic='raw_data', payload=str(data))
            # time.sleep(1)
        raw_data.clear()
    time.sleep(1)


