import ibmiotf.application
import time
import json
from sense_hat import SenseHat

options = {
    "org": "s0wlob",
    "id": "assignment1",
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

def DataCallback(event):
    print("Got event " + json.dumps(event.data))
    temperature = event.data['temperature']
    commandData = {'temperature': temperature}
    client.publishCommand(targetDeviceType, targetDeviceId, "temperature", "json", commandData)


client = ibmiotf.application.Client(options)

client.connect()
#client.deviceEventCallback = ButtonCallback()
client.deviceEventCallback = DataCallback

client.subscribeToDeviceEvents(deviceType=sourceDeviceType, deviceId=sourceDeviceId, event=sourceEvent)
