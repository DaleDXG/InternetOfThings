import paho.mqtt.client as mqtt
from sense_hat import SenseHat
import json
import time
import thread
import argparse
import ssl

host = 'knd28j.messaging.internetofthings.ibmcloud.com'
clientid = 'd:knd28j:raspberrypi:b827eb6312cc'
username = 'use-token-auth'
#passwd = '&UNH@ox)k5Sftfs3l-'
topic_h = 'iot-2/evt/'
button = 1
topic_b = ['temperature','pressure','humidity','m_x', 'm_y', 'm_z', 'compass']
topic_b_flag = [1, 1, 1, 1,1,1,1]
topic_debug_flag = [1,1,1,1,1,1,1]
topic_fmt = '/fmt/json'

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

# Define a thread detect button
def detec_button(threadName):
    global button
    sense = SenseHat()
    while True:
        for event in sense.stick.get_events():
          direction=event.direction
          action = event.action
          if action=='released':
             button=(button+1)%2
             topic='iot-2/evt/button/fmt/json'
             client.publish(topic, json.dumps({'button':button}))
             print('button'+ str(button))

def mypublish(topic_body, value):
    topic= topic_h + topic_body + topic_fmt
    for i in range(len(topic_b)):
        if topic_b[i]==topic_body:
            if topic_b_flag[i]==1:
                client.publish(topic, json.dumps({topic_body:value}))
                if topic_debug_flag[i]==1:
                    print(topic +': '+ str(value))

parser_input = argparse.ArgumentParser()
parser_input.add_argument("-p", "--pass", action="store", required=True, dest='token',help="token from ibm cloud")
args = parser_input.parse_args()
passwd=args.token
client = mqtt.Client(clientid,clean_session=True)
client.username_pw_set(username,passwd)
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(ca_certs="/home/pi/Downloads/rootCA.pem", certfile="/home/pi/Downloads/client.pem",keyfile="/home/pi/Downloads/client.key",cert_reqs=ssl.CERT_NONE)
#client.tls_set()
client.connect(host,8883, 60)
client.loop_start()
sense = SenseHat()

try:
   thread.start_new_thread( detec_button, ("Thread-1", ) )
except:
   print "Error: unable to start thread"

while	True:
    try:
        h = sense.get_humidity()
        mypublish('humidity', h)

        t = sense.get_temperature()
        mypublish('temperature', t)

        p = sense.get_pressure()
        mypublish('pressure', p)


        topic='iot-2/evt/button/fmt/json'
        client.publish(topic, json.dumps({'button':button}))
        print('button: ' + str(button))

        compass_data = sense.get_compass_raw()
        m_x = compass_data['x']
        m_y = compass_data['y']
        m_z = compass_data['z']
        mypublish('m_x', m_x)
        mypublish('m_y', m_y)
        mypublish('m_z', m_z)

        north = sense.get_compass()
        print('north: '+ str(north))

        topic='iot-2/evt/compass/fmt/json'
        client.publish(topic,json.dumps({'x':m_x, 'y':m_y, 'z':m_z, 'north':north}))

        time.sleep(1)
    except IOError:
        print ("Error")
