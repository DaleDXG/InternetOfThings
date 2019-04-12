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
client.connect(host, 1883, 60)

sense = SenseHat()

while True:
    try:
        t_h = sense.get_temperature_from_humidity()
        t_p = sense.get_temperature_from_pressure()
        h = sense.get_humidity()
        p = sense.get_pressure()
        
        client.publish(topic, json.dumps({'t_h':t_h,'t_p':t_p,'h':h,'p':p}))
        #print('' + str(t_h) + '\n' + str(t_p )+ '\n' + str(h) + '\n' + str(p) + '\n')
        time.sleep(.5)
    except IOError:
        print("IOError")

client.loop()
client.disconnect()
