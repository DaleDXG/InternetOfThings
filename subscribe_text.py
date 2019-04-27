import time
import json
import paho.mqtt.client as mqtt
#from sense_hat import SenseHat
import ssl

# MQTT parameters
host = 's0wlob.messaging.internetofthings.ibmcloud.com'
clientid = 'd:s0wlob:Display:LED'
username = 'use-token-auth'
password = 'K-Tx+D)0CKnF+*Hot)'
topic = 'iot-2/evt/text/fmt/json'

#sense = SenseHat()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

def on_message(client, userdata, msg):
    print('message')
    print(msg.payload)
    msg = json.loads(msg.payload)["msg"]
    #sense.show_message(msg)

client = mqtt.Client(clientid)
client.username_pw_set(username, password)
client.tls_set()
client.connect(host, 8883, 60)
client.subscribe(topic)
client.on_connect = on_connect
client.on_message = on_message
client.loop_start()

while True:  
    time.sleep(5)