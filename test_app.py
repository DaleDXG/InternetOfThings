import time
import json
import paho.mqtt.client as mqtt
import ibmiotf.application

# MQTT parameters
host = 'scq23v.messaging.internetofthings.ibmcloud.com'
clientid = 'a:scq23v:app01'
username = 'a-scq23v-fo4saykkqw'
password = 'Lvm-aocsayEUCoUjQp'
topic = 'iot-2/cmd/weather/fmt/json'

options = {
    "org": "scq23v",
    "id": "app01",
    "auth-method": "apikey",
    "auth-key": "a-scq23v-fo4saykkqw",
    "auth-token": "Lvm-aocsayEUCoUjQp",
    "clean-session": True
}

sourceDeviceType = "InfoPublisher"
sourceDeviceId = "WeatherPublisher"
sourceEvent = "weather"

targetDeviceType = "InfoSubscriber"
targetDeviceId = "WeatherSubscriber"

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