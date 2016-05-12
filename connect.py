import signal
import time
import sys
import json
import ibmiotf.application

def myEventCallback(myEvent):
  print("%-33s%-32s%s: %s" % (myEvent.timestamp.isoformat(), myEvent.device, myEvent.event, json.dumps(myEvent.data)))

def interruptHandler(signal, frame):
  client.disconnect()
  sys.exit(0)


options = {
  "org": "a1bl4a",
  "id": "leddy2",
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

print("(Press Ctrl+C to disconnect)")
client.deviceEventCallback = myEventCallback
client.subscribeToDeviceEvents(deviceType="Rater")

while True:
  time.sleep(1)
