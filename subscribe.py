import time
import json
import paho.mqtt.client as mqtt
from sense_hat import SenseHat

# MQTT parameters
host = 's0wlob.messaging.internetofthings.ibmcloud.com'
clientid = 'a:s0wlob:showTemperatureOnLED'
username = 'a-s0wlob-ujrxjcezwv'
password = 'O7-Feqo2w_ye0SzhNe'
topic_start = 'iot-2/type/Sensors/id/SenseHAT/evt/
topic_mid = 'temperature'
topic_end = '/fmt/json'
topic = topic_start + topic_mid + topic_end
# #username = 'use-token-auth'
# #password = 'MA+BJELzPCj2N(rQI4'
# topic = 'iot-2/type/Sensors/id/SenseHAT/evt/temperature/fmt/json'
# #topic = 'iot-2/cmd/temperature/fmt/json'
sense = SenseHat()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic)


def on_message(client, userdata, msg):
    
    temperature = json.loads(msg.payload)["temperature"]
    print(temperature)
    sense.show_message(str(temperature))


client = mqtt.Client(clientid)
client.username_pw_set(username, password)
client.tls_set()
client.connect(host, 8883, 60)
client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()
