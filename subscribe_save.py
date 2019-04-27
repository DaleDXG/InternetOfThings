import time
import json
import paho.mqtt.client as mqtt
from sense_hat import SenseHat

# MQTT parameters
host = 's0wlob.messaging.internetofthings.ibmcloud.com'
clientid = 'a:s0wlob:showTemperatureOnLED'
username = 'a-s0wlob-ujrxjcezwv'
password = 'O7-Feqo2w_ye0SzhNe'

# Topic set
topic_start = 'iot-2/type/Sensors/id/SenseHAT/evt/'
topic_list = ['temperature', 'humidity', 'pressure', 'compass', 'message']
# topic_mid = 'temperature'
topic_end = '/fmt/json'

num_topic = 0
len_topic = len(topic_list)

# #username = 'use-token-auth'
# #password = 'MA+BJELzPCj2N(rQI4'
# topic = 'iot-2/type/Sensors/id/SenseHAT/evt/temperature/fmt/json'
# #topic = 'iot-2/cmd/temperature/fmt/json'
sense = SenseHat()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    for i in range(len(topic_list)):
        topic_mid = topic_list[i]
        topic = topic_start + topic_mid + topic_end        
        client.subscribe(topic)
        #print('topic: ' + str(topic))


def on_message(client, userdata, msg):
    #print(msg.payload)
    print(num_topic)
    topic_show = topic_list[num_topic]
    
    if topic_show == 'temperature':      
        temperature = json.loads(msg.payload)["temperature"]
        print(temperature)
        sense.show_message('T: ' + str(temperature))
        
     
               
    elif topic_show == 'humidity':      
        humidity = json.loads(msg.payload)["humidity"]
        print(humidity)
        sense.show_message('H: ' + str(humidity))
        
    # new add
    elif topic_show == 'pressure':
        pressure = json.loads(msg.payload)["pressure"]
        print(topic_show + pressure)
        sense.show_message('P: ' + str(pressure))
    elif topic_show == 'compass'：
        m_x = json.loads(msg.payload)["m_x"]
        m_y = json.loads(msg.payload)["m_y"]
        m_z = json.loads(msg.payload)["m_z"]
        north = json.loads(msg.payload)["north"]
        print('North: ' + str(north) + ' Compass_x: ' + str(m_x) + ' Compass_y: ' + str(m_y) + ' Compass_z: ' + str(m_z))
        #sense.show_message('North: ' + str(north) + ' x: ' + str(m_x) + ' y: ' + str(m_y) + ' z: ' + str(m_z))
        sense.show_message('North: ' + str(north))
    elif topic_show == 'message':
        message = json.loads(msg.payload)["msg"]
        print(message)
        sense.show_message(message)
#     topic_value = json.loads(msg.payload)[topic_show]
#     print(topic_show + ': ' + value)
#     sense.show_message(str(value))


client = mqtt.Client(clientid)
client.username_pw_set(username, password)
client.tls_set()
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
