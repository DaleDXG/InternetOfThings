import sys
import time
import json
import paho.mqtt.client as mqtt
import ssl
import argparse

# MQTT parameters
host = 's0wlob.messaging.internetofthings.ibmcloud.com'
clientid = 'd:s0wlob:Sensors:SenseHAT'
username = 'use-token-auth'
password = '9q@)ZLnq@Fc?348(Lk'
topic = 'iot-2/evt//fmt/json'

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

#parser_input = argparse.ArgumentParser()  # the token is used to security check
#parser_input.add_argument("-p", "--pass", action="store", required=True, dest='token',help="token from ibm cloud")
#args = parser_input.parse_args()
#password = args.token

client = mqtt.Client(clientid)
client.username_pw_set(username, password)
client.on_connect = on_connect
client.tls_set(ca_certs='/home/pi/Code/rootCA.pem', certfile='/home/pi/Code/client.pem', keyfile='/home/pi/Code/client.key')
client.connect(host, 8883, 60)

while True:
    try:
        strJson = json.dumps({'msg': 'Congraduations!'})
        client.publish(topic, strJson)
        print(strJson)
        time.sleep(5)
    except IOError:
        print("IOError")

client.loop()
client.disconnect()