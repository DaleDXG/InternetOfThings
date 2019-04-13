import ibmiotf.application
import time
import json
from sense_hat import SenseHat

options = {
    "org": "s0wlob",
    "id": "assignment1",
    "auth-method": "apikey",
    "auth-key": "a-s0wlob-mv8vlr5oei",
    "auth-token": "z78d0999HjMoyTc-n3",
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
client.deviceEventCallback = DataCallback()

client.subscribeToDeviceEvents(deviceType=sourceDeviceType, deviceId=sourceDeviceId, event=sourceEvent)
