from sense_hat import SenseHat

import paho.mqtt.client as mqtt
import struct
import json1

sense = SenseHat()
sense.clear()

t_h = sense.get_temperature_from_humidity()
t_p = sense.get_temperature_from_pressure()
h = sense.get_humidity()
p = sense.get_pressure()
#print(t_h)
#print(t_p)
#print(h)
#print(p)