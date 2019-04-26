import time
import json
import paho.mqtt.client as mqtt
from sense_hat import SenseHat
import MySQLdb
import ssl

# MQTT parameters
host = 's0wlob.messaging.internetofthings.ibmcloud.com'
clientid = 'a:s0wlob:showTemperatureOnLED'
username = 'a-s0wlob-ujrxjcezwv'
password = 'O7-Feqo2w_ye0SzhNe'

# Topic set
topic_start = 'iot-2/type/Sensors/id/SenseHAT/evt/'
topic_list = ['temperature', 'humidity', 'pressure', 'compass', 'hello']
topic_end = '/fmt/json'

num_topic = 0
len_topic = len(topic_list)

sense = SenseHat()


db = MySQLdb.connect("localhost", "iot", "password", "ass1")
curs = db.cursor()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    for i in range(len(topic_list)):
        topic_mid = topic_list[i]
        topic = topic_start + topic_mid + topic_end        
        client.subscribe(topic)
        print('topic: ' + str(topic))


def on_message(client, userdata, msg):
    print(msg.payload)
    print(num_topic)
    topic_show = topic_list[num_topic]
    
    if topic_show == 'hello':      
        msg = json.loads(msg.payload)["msg"]
        print(msg)
        sense.show_message(msg)  
#         temperature = round(temperature, 1)
#         try:
#             curs.execute("""INSERT INTO temperature
#                     values(now(), %s)""", (temperature,))
#             db.commit()
#             print("Data commited")
#         except:
#             print("Error: the database is being rolled back")
#             db.rollback()
    
    if topic_show == 'temperature':      
        temperature = json.loads(msg.payload)["temperature"]
        print(temperature)
        sense.show_message('T: ' + str(temperature))  
        temperature = round(temperature, 1)
        try:
            curs.execute("""INSERT INTO temperature
                    values(now(), %s)""", (temperature,))
            db.commit()
            print("Data commited")
        except:
            print("Error: the database is being rolled back")
            db.rollback()
        
    elif topic_show == 'humidity':      
        humidity = json.loads(msg.payload)["humidity"]
        print(humidity)
        sense.show_message('H: ' + str(humidity))
        # new add
        humidity = round(humidity, 1)
        try:
            curs.execute("""INSERT INTO humidity
                    values(now(), %s)""", (humidity,))
            db.commit()
            print("Data commited")
        except:
            print("Error: the database is being rolled back")
            db.rollback()
    elif topic_show == 'pressure':
        pressure = json.loads(msg.payload)["pressure"]
        print(pressure)
        sense.show_message('P: ' + str(pressure))
        # new add
        pressure = round(pressure, 1)
        try:
            curs.execute("""INSERT INTO pressure
                    values(now(), %s)""", (pressure,))
            db.commit()
            print("Data commited")
        except:
            print("Error: the database is being rolled back")
            db.rollback()
    elif topic_show == 'compass':
        m_x = json.loads(msg.payload)["m_x"]
        m_y = json.loads(msg.payload)["m_y"]
        m_z = json.loads(msg.payload)["m_z"]
        north = json.loads(msg.payload)["north"]
        print('North: ' + str(north) + ' Compass_x: ' + str(m_x) + ' Compass_y: ' + str(m_y) + ' Compass_z: ' + str(m_z))
        sense.show_message('North: ' + str(north) + ' x: ' + str(m_x) + ' y: ' + str(m_y) + ' z: ' + str(m_z))
        # new add
        m_x = round(m_x, 1)
        m_y = round(m_y, 1)
        m_z = round(m_z, 1)
        try:
            curs.execute("""INSERT INTO compass
                    values(now(), %s, %s, %s)""", (m_x, m_y, m_z))
            db.commit()
            print("Data commited")
        except:
            print("Error: the database is being rolled back")
            db.rollback()
        
#     topic_value = json.loads(msg.payload)[topic_show]
#     print(topic_show + ': ' + value)
#     sense.show_message(str(value))

client = mqtt.Client(clientid)
client.username_pw_set(username, password)
client.tls_set(ca_certs='/home/pi/Code/rootCA.pem', certfile='/home/pi/Code/client.pem', keyfile='/home/pi/Code/client.key')
client.connect(host, 8883, 60)
client.on_connect = on_connect
client.on_message = on_message
client.loop_start()

while True:  
    for event in sense.stick.get_events():
        action = event.action
        if action == 'released':
            num_topic = (num_topic + 1) % len_topic
            sense.clear()
