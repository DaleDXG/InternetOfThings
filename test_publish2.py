import sys
import time
import json
import paho.mqtt.client as mqtt
from sense_hat import SenseHat


# MQTT parameters
host = 's0wlob.messaging.internetofthings.ibmcloud.com'
clientid = 'd:s0wlob:Sensors:SenseHAT'
username = 'use-token-auth'
password = '9q@)ZLnq@Fc?348(Lk'
topic = 'iot-2/evt/temperature/fmt/json'

client = mqtt.Client(clientid)
client.username_pw_set(username, password)
client.tls_set()
client.connect(host, 8883, 60)


sense = SenseHat()
while True:
    try:
        t_h = sense.get_temperature_from_humidity()
        strJson = json.dumps({'temperature': t_h})
        client.publish(topic, strJson)
        print(strJson)
        time.sleep(2)
    except IOError:
        print("IOError")

client.loop()
client.disconnect()
