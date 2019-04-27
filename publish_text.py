import sys
import time
import json
import paho.mqtt.client as mqtt
import argparse
import ibmiotf.application

# MQTT parameters
host = 's0wlob.messaging.internetofthings.ibmcloud.com'
clientid = 'a:s0wlob:text'
username = 'a-s0wlob-4mmbxx2owp'
password = 'xs1Wd-I)z_wfjdZWtQ'
topic = 'iot-2/type/Display/id/LED/cmd/text/fmt/json'

client = mqtt.Client(clientid)
client.username_pw_set(username, password)
client.tls_set()
client.connect(host, 8883, 60)

parser_input = argparse.ArgumentParser()  # the token is used to security check
parser_input.add_argument("-t", "--text", action="store", required=True, dest='text',help="text for printing")
args = parser_input.parse_args()
text = args.text
client.loop()

try:
    strJson = json.dumps({'msg': text})
    client.publish(topic, strJson)
    print(strJson)
except IOError:
    print("IOError")
    
client.disconnect()