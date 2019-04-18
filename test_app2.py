import time
import json
import paho.mqtt.client as mqtt
import ibmiotf.application

options = {
    "org": "s0wlob",
    "id": "showTemperatureOnLED",
    "auth-method": "apikey",
    "auth-key": "a-s0wlob-ujrxjcezwv",
    "auth-token": "O7-Feqo2w_ye0SzhNe",
    "clean-session": True
}

sourceDeviceType = "Sensors"
sourceDeviceId = "SenseHAT"
sourceEvent = "temperature"

targetDeviceType = "Display"
targetDeviceId = "LED"

def myEventCallback(event):
    print("Got event " + json.dumps(event.data))
    #temperature = event.data['temperature']
    commandData = event.data #{'temperature': temperature}
    client.publishCommand(targetDeviceType, targetDeviceId, "weather", "json", commandData)

try:
    client = ibmiotf.application.Client(options)
except ibmiotf.ConnectionException as e:
    print(e)
client.connect()
#client.deviceEventCallback = ButtonCallback()
client.deviceEventCallback = myEventCallback
client.subscribeToDeviceEvents(deviceType=sourceDeviceType, deviceId=sourceDeviceId, event=sourceEvent)

while True:
    #commandData = {"temperature": 10, "humidity": 25}
    #client.publishCommand(targetDeviceType, targetDeviceId, "weather", "json", commandData)
    time.sleep(1)