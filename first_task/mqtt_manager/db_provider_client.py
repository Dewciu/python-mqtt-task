from paho.mqtt.client import Client
from mqtt_manager import broker
from db_provider.db_provider import DbProvider
import json

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)

def on_message(client, userdata, message):
    received_json_data = message.payload.decode('UTF-8')
    json_acceptable_data = received_json_data.replace("'", "\"")
    received_json_dict_data = json.loads(json_acceptable_data)
    dbprovider.provide_to_database(received_json_dict_data)

client_name = 'db_provider'
client = Client(client_name)
client.on_connect = on_connect
print("Connecting to broker ", broker)
client.connect(broker)
client.subscribe(topic='json_data')
client.on_message = on_message

dbprovider = DbProvider()

client.loop_forever()