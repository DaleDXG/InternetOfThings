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
topic = 'iot-2/evt/'

client = mqtt.Client(clientid)
client.username_pw_set(username, password)
client.tls_set()
client.connect(host, 8883, 60)

sense = SenseHat()

while True:
    try:
        # get temperature data
        temp = sense.get_temperature()
        temp = round(temp, 1)
        top_tem = topic + 'temperature/fmt/json'
        client.publish(top_tem, json.dumps({'temperature': temp}))
        print('Temperature: ' + str(temp) + '; ')

        # get humidity data
        hum = sense.get_humidity()
        hum = round(hum, 1)
        top_hum = topic + 'humidity/fmt/json'
        client.publish(top_hum, json.dumps({'humidity': hum}))
        print('Humidity: ' + str(hum) + '; ')

        # get pressure data
        pre = sense.get_pressure()
        pre = round(pre, 1)
        top_pre = topic + 'pressure/fmt/json'
        client.publish(top_pre, json.dumps({'pressure': pre}))
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
        top_com = topic + 'compass/fmt/json'
        client.publish(top_com, json.dumps({'north':compass_north,'m_x': m_x, 'm_y': m_y, 'm_z': m_z}))
        print('North: ' + str(compass_north) + ' Compass_x: ' + str(m_x) + ' Compass_y: ' + str(m_y) + ' Compass_z: ' + str(m_z) + '\n')

        # joystick
        top_joy = topic + 'joystick/fmt/json'
        for event in sense.stick.get_events():
            client.publish(top_joy, json.dumps({'direction': event.direction, 'action': event.action}))
            print('Joystick_direction: ' + event.direction + ' Joystick_action: ' + event.action)

        time.sleep(1)

    except IOError:
        print("IOError")

client.loop()
client.disconnect()
