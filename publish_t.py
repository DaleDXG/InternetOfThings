import time
import json
import argparse
import ibmiotf.application

try:
  options = {
    "org": "s0wlob",
    "id": "text",
    "auth-method": "apikey",
    "auth-key": "a-s0wlob-4mmbxx2owp",
    "auth-token": "xs1Wd-I)z_wfjdZWtQ",
    "clean-session": True
  }
  client = ibmiotf.application.Client(options)
except ibmiotf.ConnectionException as e:
    print(e)

#
parser_input = argparse.ArgumentParser()  # the token is used to security check
parser_input.add_argument("-t", "--text", action="store", required=True, dest='text',help="text for printing")
args = parser_input.parse_args()
text = args.text

deviceType = 'Display'
deviceId = 'LED'

client.connect()
myData={'msg' : text}
#while True:
client.publishCommand(deviceType, deviceId, "text", "json", myData)