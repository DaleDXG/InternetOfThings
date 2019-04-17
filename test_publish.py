import sys
import time
import json
import paho.mqtt.client as mqtt

# MQTT parameters
host = 'scq23v.messaging.internetofthings.ibmcloud.com'
clientid = 'd:scq23v:InfoPublisher:WeatherPublisher'
username = 'use-token-auth'
password = 'o@5H?JLXQtWO!!AKEH'
topic = 'iot-2/evt/weather/fmt/json'

client = mqtt.Client(clientid)
client.username_pw_set(username, password)
client.tls_set()
client.connect(host, 8883, 60)

while True:
    try:
        strJson = json.dumps({'temperature': 16, 'humidity': 30})
        client.publish(topic, strJson)
        print(strJson)
        time.sleep(2)
    except IOError:
        print("IOError")

client.loop()
client.disconnect()