import ibmiotf.application
import time
import json

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

def ButtonCallback(event):
    print("Got event " + json.dumps(event.data))
    button = event.data['Button']
    commandData = {'state': button}
    client.publishCommand(targetDeviceType, targetDeviceId, "state", "json", commandData)

client = ibmiotf.application.Client(options)

client.connect()
#client.deviceEventCallback = ButtonCallback()

client.subscribeToDeviceEvents(deviceType=sourceDeviceType, deviceId=sourceDeviceId, event=sourceEvent)