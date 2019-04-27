import paho.mqtt.client as mqtt
import json
import time
import argparse
import ssl

host = 's0wlob.messaging.internetofthings.ibmcloud.com'
clientid = 'd:s0wlob:Sensors:SenseHAT'
username = 'use-token-auth'
passwd = '9q@)ZLnq@Fc?348(Lk'
topic = 'iot-2/evt/D/fmt/json'

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client(clientid,clean_session=True)
client.username_pw_set(username,passwd)
client.on_connect = on_connect
client.on_message = on_message
# 3 key files are used to authentication
client.tls_set(ca_certs="rootCA.pem", certfile="client.pem",keyfile="client.key")
client.connect(host,8883, 60)
client.loop_start()

while	True:
    try:
        strJson = json.dumps({'msg': 'Congraduations! You have finished ass1.'})
        client.publish(topic, strJson)
        time.sleep(5)
    except IOError:
        print ("Error")
