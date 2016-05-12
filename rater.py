import time
import sys
import ibmiotf.application
import ibmiotf.device
import random #for random rating values from 1 to 5

deviceOptions = {
  "org": "a1bl4a",
  "type": "Rater",
  "id": "PC",
  "auth-method": "token",
  "auth-token": "qwertyuiop"
}

try:
  deviceCli = ibmiotf.device.Client(deviceOptions)
except Exception as e:
  print("Caught exception connecting device: %s" % str(e))
  sys.exit()

deviceCli.connect()
for x in range (0,10):
  data = { 'Rating' : random.randrange(1,6)}
  deviceCli.publishEvent("Rating", "json", data)
  time.sleep(10)

deviceCli.disconnect()
