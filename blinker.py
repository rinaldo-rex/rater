import ibmiotf.application
import ibmiotf.device
import sys
import time

options = {
  "org": "a1bl4a",
  "id": "leddy1",
  "auth-method": "apikey",
  "auth-key": "a-a1bl4a-qkxmthdvws",
  "auth-token": "C+@qBdNsvo6bwu6@w3"
}

try:
  client = ibmiotf.application.Client(options)
  client.connect()
except Exception as e:
  print(str(e))
  sys.exit()

myDeviceType = "Rater"

def myEventCallback(event):
  str = "%s event '%s' received from device [%s]: %s"
  print(str % (event.format, event.event, event.device, json.dumps(event.data)))

client.connect()
client.deviceEventCallback = myEventCallback
# client.subscribeToDeviceEvents()
client.subscribeToDeviceEvents(deviceType=myDeviceType)

while True:
  time.sleep(1)
