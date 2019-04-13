import json
import paho.mqtt.client as mqtt
from sense_hat import SenseHat

# MQTT parameters
host = 's0wlob.messaging.internetofthings.ibmcloud.com'
clientid = 'd:s0wlob:Sensors:SenseHAT'
username = 'use-token-auth'
password = '9q@)ZLnq@Fc?348(Lk'
topic = 'iot-2/type/Sensors/id/SenseHAT/temperature/fmt/json'
sense = SenseHat()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    

def on_message(client, userdata, msg):
    temperature = json.loads(msg.payload)["temperature"]
    print(temperature)
    sense.show_message(str(temperature))


client = mqtt.Client(clientid)
client.username_pw_set(username, password)
client.connect(host, 1883, 60)
client.subscribe(topic)
client.on_connect = on_connect
client.on_message = on_message
client.loop_forever
