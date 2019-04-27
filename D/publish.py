import sys
import time
import json
import threading
import paho.mqtt.client as mqtt
import ssl
from sense_hat import SenseHat

# MQTT parameters
host = 's0wlob.messaging.internetofthings.ibmcloud.com'
clientid = 'd:s0wlob:Sensors:SenseHAT'
username = 'use-token-auth'
password = '9q@)ZLnq@Fc?348(Lk'
topic_h = 'iot-2/evt/'
topic_fmt = '/fmt/json'

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("on_message")
    text = json.loads(msg.payload)["msg"]
    print(text)
    #print(msg.topic+" "+str(msg.payload))

# thread for joy stick
def publishJoystick():
    sense = SenseHat()
    while True:
        for event in sense.stick.get_events():
          direction = event.direction
          action = event.action
          if action=='pressed' or action=='released':
             topic='iot-2/evt/joystick/fmt/json'
             client.publish(topic, json.dumps({'direction':direction, 'action':action}))
             print('joystick:'+ direction + ',' + action)

def publishOtherInfo():
    sense = SenseHat()
    while True:
        try:
            # get temperature data
            temp = sense.get_temperature()
            temp = round(temp, 1)
            publish('temperature', {'temperature': temp})
            print('Temperature: ' + str(temp) + '; ')

            # get humidity data
            hum = sense.get_humidity()
            hum = round(hum, 1)
            publish('humidity', {'humidity': hum})
            print('Humidity: ' + str(hum) + '; ')

            # get pressure data
            pre = sense.get_pressure()
            pre = round(pre, 1)
            publish('pressure', {'pressure': pre})
            print('Pressure: ' + str(pre))

            # get compass data
            compass_north = sense.get_compass()
            compass_north = round(compass_north, 1)
            compass_data = sense.get_compass_raw()
            m_x = compass_data['x']
            m_x = round(m_x, 1)
            m_y = compass_data['y']
            m_y = round(m_y, 1)
            m_z = compass_data['z']
            m_z = round(m_z, 1)
            publish('compass', {'north':compass_north,'m_x': m_x, 'm_y': m_y, 'm_z': m_z})
            print('North: ' + str(compass_north) + ' Compass_x: ' + str(m_x) + ' Compass_y: ' + str(m_y) + ' Compass_z: ' + str(m_z) + '\n')

            time.sleep(3)

        except IOError:
            print("IOError")

def publish(topic, data):
    topic= topic_h + topic + topic_fmt
    client.publish(topic, json.dumps(data))

client = mqtt.Client(clientid)
client.username_pw_set(username, password)
client.on_connect = on_connect
client.on_message = on_message
client.tls_set()
#client.tls_set(ca_certs='rootCA.pem', certfile='client.pem', keyfile='client.key', cert_reqs=ssl.CERT_NONE)
client.connect(host, 8883, 60)
client.subscribe('iot-2/cmd/text/fmt/json', 2)

try:
   thread_joystick = threading.Thread(target = publishJoystick, name = 'thread_joystick')
   thread_joystick.start()
   thread_otherInfo = threading.Thread(target = publishOtherInfo, name = 'thread_otherInfo')
   thread_otherInfo.start()
except:
   print("Error: unable to start thread")

client.loop_forever()