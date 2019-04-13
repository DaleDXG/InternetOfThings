import time
import json
import paho.mqtt.client as mqtt
from sense_hat import SenseHat

# MQTT parameters
host = 's0wlob.messaging.internetofthings.ibmcloud.com'
clientid = 'd:s0wlob:Sensors:SenseHAT'
username = 'use-token-auth'
password = '9q@)ZLnq@Fc?348(Lk'
topic = 'iot-2/cmd/temperature/fmt/json'


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

def on_message(client, userdata, msg):
    button = json.loads(msg.payload)["state"]
    if button == "on":
        grovepi.digitalWrite(led,1)
    else:
        grovepi.digitalQrite(led,0)
    print(button)



client = mqtt.Client(clientid)
client.username_pw_set(username, password)
client.connect(host, 1883, 60)
client.subscribe(topic)
client.on_connect = on_connect
client.on_message = on_message
client.loop_forever

# 以上代码是视频中的

sense = SenseHat()

while True:
    try:
        # get temperature data
        t_h = sense.get_temperature_from_humidity()
        t_p = sense.get_temperature_from_pressure()
        top_tem = topic + 'temperature/fmt/json'
        client.publish(top_tem, json.dumps({'temperature': t_h}))
        print('Temperature: ' + str(t_h) + '\n')

        # get humidity data
        h = sense.get_humidity()
        top_hum = topic + 'humidity/fmt/json'
        client.publish(top_hum, json.dumps({'humidity': h}))
        print('Humidity: ' + str(h) + '\n')

        # get pressure data
        p = sense.get_pressure()
        top_pre = topic + 'pressure/fmt/json'
        client.publish(top_pre, json.dumps({'pressure': p}))
        print('Pressure: ' + str(p) + '\n')

        # get compass data
        compass_data = sense.get_compass_raw()
        m_x = compass_data['x']
        m_y = compass_data['y']
        m_z = compass_data['z']
        top_com = topic + 'compass/fmt/json'
        client.publish(top_com, json.dumps({'m_x': m_x, 'm_y': m_y, 'm_z': m_z}))
        print('Compass_x: ' + str(m_x) + ' Compass_y: ' + str(m_y) + ' Compass_z: ' + str(m_z) + '\n')

        time.sleep(1)

        # joystick
        top_joy = topic + 'joystick/fmt/json'
        for event in sense.stick.get_events():
            client.publish(top_joy, json.dumps({'direction': event.direction, 'action': event.action}))
            print('Joystick_direction: ' + event.direction + ' Joystick_action: ' + event.action)

    except IOError:
        print("IOError")

client.loop()
client.disconnect()
