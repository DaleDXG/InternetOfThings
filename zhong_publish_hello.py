import sys
import time
import json
import paho.mqtt.client as mqtt
from sense_hat import SenseHat

# MQTT parameters
host = 's0wlob.messaging.internetofthings.ibmcloud.com'
clientid = 'd:s0wlob:Display:hello'
username = 'use-token-auth'
password = 'yR4w+qpnbB2v4fV4R3'
topic = 'iot-2/evt/hello/fmt/json'

client = mqtt.Client(clientid)
client.username_pw_set(username, password)
client.tls_set()
client.connect(host, 8883, 60)

while True:
    try:
        strJson = json.dumps({'msg': 'Congraduations! You have finished ass1.'})
        client.publish(topic, strJson)
        print(strJson)
        time.sleep(2)
    except IOError:
        print("IOError")

client.loop()
client.disconnect()