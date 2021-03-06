import time
import json
import paho.mqtt.client as mqtt
from sense_hat import SenseHat
import MySQLdb
import ssl
import threading

# MQTT parameters
host = 's0wlob.messaging.internetofthings.ibmcloud.com'
clientid = 'a:s0wlob:showTemperatureOnLED'
username = 'a-s0wlob-ujrxjcezwv'
password = 'O7-Feqo2w_ye0SzhNe'

# Topic set
topic_h = 'iot-2/type/Sensors/id/SenseHAT/evt/'
topic_list = ['temperature', 'humidity', 'pressure', 'compass', 'joystick', 'text']
topic_fmt = '/fmt/json'

db = MySQLdb.connect("localhost", "iot", "password", "ass1")
curs = db.cursor()

_temperature = 0
_humidity = 0
_pressure = 0
_north = 0
_m_x = 0
_m_y = 0
_m_z = 0
_direction = ''
_action = ''
_text = ''

def save_data(tableName, data):
    try:
        sql_str = "INSERT INTO " + str(tableName) + " values(now(), "
        for d in data:
            sql_str = sql_str + str(d) + ', '
        sql_str = sql_str[:-2] + ')'
        #print(sql_str)
        curs.execute(sql_str)
        db.commit()
    except:
        print("Error: the database is being rolled back")
        db.rollback()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    """ topic_ls = []
    for i in range(len(topic_list)):
        topic = topic_h + topic_list[i] + topic_fmt
        topic_ls.append((topic, i))
        print('topic: ' + str(topic))
    client.subscribe(topic_ls) """
    for i in range(len(topic_list)):
        topic = topic_h + topic_list[i] + topic_fmt
        client.subscribe(topic)
        print('topic: ' + str(topic))
    client.subscribe('iot-2/type/Sensors/id/SenseHAT/cmd/text/fmt/json')


def on_message(client, userdata, msg):
    global _temperature
    global _humidity
    global _pressure
    global _north
    global _m_x
    global _m_y
    global _m_z
    global _direction
    global _action
    global _text
    #print(msg.payload)
    if str(msg.topic).find('temperature') != -1:
        temperature = json.loads(msg.payload)["temperature"]
        print("temperature: " + str(temperature))
        _temperature = temperature
        save_data("temperature", [temperature])
    elif msg.topic.find('humidity') != -1:
        humidity = json.loads(msg.payload)["humidity"]
        print("humidity: " + str(humidity))
        _humidity = humidity
        save_data("humidity", [humidity])
    elif msg.topic.find('pressure') != -1:
        pressure = json.loads(msg.payload)["pressure"]
        print("pressure: " + str(pressure))
        _pressure = pressure
        save_data("pressure", [pressure])
    elif msg.topic.find('compass') != -1:
        m_x = json.loads(msg.payload)["m_x"]
        print("m_x: " + str(m_x))
        _m_x = m_x
        m_y = json.loads(msg.payload)["m_y"]
        print("m_y: " + str(m_y))
        _m_y = m_y
        m_z = json.loads(msg.payload)["m_z"]
        print("m_z: " + str(m_z))
        _m_z = m_z
        north = json.loads(msg.payload)["north"]
        print("north: " + str(north))
        _north = north
        save_data("compass", [m_x, m_y, m_z])
    elif msg.topic.find('text') != -1:
        text = json.loads(msg.payload)["msg"]
        print("text: " + str(text))
        _text = text
        save_data("message", [text])
    elif msg.topic.find('joystick') != -1:
        direction = json.loads(msg.payload)["direction"]
        print("direction: " + str(direction))
        _direction = direction
        action = json.loads(msg.payload)["action"]
        print("action: " + str(action))
        _action = action

client = mqtt.Client(clientid)
client.username_pw_set(username, password)
client.on_connect = on_connect
client.on_message = on_message
client.tls_set()
client.connect(host, 8883, 60)

def showMessage():
    sense = SenseHat()
    sense.clear()
    while True:
        if _direction == 'left':
            sense.show_message('T: ' + str(_temperature), text_colour = [255, 0, 0])
        elif _direction == 'right':
            sense.show_message('H: ' + str(_humidity), text_colour = [0, 255, 0])
        elif _direction == 'up':
            sense.show_message('P: ' + str(_pressure), text_colour = [0, 0, 255])
        elif _direction == 'down':
            sense.show_message('Text: ' + str(_text), text_colour = [255, 0, 255])
        elif _direction == 'middle':
            #sense.clear()
            sense.show_message('m_x: ' + str(_m_x) + 'm_y: ' + str(_m_y) + 'm_z: ' + str(_m_z), text_colour = [0, 255, 255])
        time.sleep(1)

try:
   thread_showMessage = threading.Thread(target = showMessage, name = 'thread_showMessage')
   thread_showMessage.start()
except:
   print("Error: unable to start thread")

client.loop_forever()
