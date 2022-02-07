import time
from lib.umqtt import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
esp.osdebug(None) 
import gc
gc.collect()

ssid = ''
password = ''
mqtt_server = '192.168.xx.xx'
client_id = ubinascii.hexlify(machine.unique_id())
topic_pub = b'' 
topic_sub = b''

last_message = 0
message_interval = 5
counter = 0

wlan = network.WLAN(network.STA_IF)

wlan.active(True)
wlan.connect(ssid, password)

while wlan.isconnected() == False:
  pass

print('Connection successful')
print(wlan.ifconfig())

