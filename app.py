import ibmiotf.application
import time
import json

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
    temperature = event.data['temperature']
    commandData = {'temperature': temperature}
    client.publishCommand(targetDeviceType, targetDeviceId, "temperature", "json", commandData)

try:
    client = ibmiotf.application.Client(options)
except ibmiotf.ConnectionException as e:
    print(e)
client.connect()
#client.deviceEventCallback = ButtonCallback()
client.deviceEventCallback = myEventCallback
client.subscribeToDeviceEvents(deviceType=sourceDeviceType, deviceId=sourceDeviceId, event=sourceEvent)

while True:
    time.sleep(1)