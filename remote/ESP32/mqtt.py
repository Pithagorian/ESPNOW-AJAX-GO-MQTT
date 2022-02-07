import network
import random
from esp import espnow
from time import sleep
from machine import Pin
# A WLAN interface must be active to send()/recv()
wlan = network.WLAN(network.STA_IF)  # Or network.AP_IF
wlan.active(True)

def sub_cb(topic, msg):
    a = int(msg.decode("utf-8"))
    if a < 4 and a >= 0:             # msg == None if timeout in irecv()
        for i in range(4):
            Leds[i].value(0)
            Leds[a].value(1)
    elif ind == -1:
        for i in range(4):
            Leds[i].value(0) 

def connect():
  global client_id, mqtt_server, topic
  client = MQTTClient(client_id, mqtt_server)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

try:
  client = connect()
except OSError as e:
  restart_and_reconnect()

Buttons = [Pin(17, Pin.IN, Pin.PULL_UP),  #groen
        Pin(16, Pin.IN, Pin.PULL_UP),  #blauw
        Pin(4, Pin.IN, Pin.PULL_UP),  #geel
        Pin(15, Pin.IN, Pin.PULL_UP)]  #wit

Leds = [Pin(13, Pin.OUT),  #groen
        Pin(12, Pin.OUT),  #blauw
        Pin(14, Pin.OUT),  #geel
        Pin(27, Pin.OUT)]  #wit

def on_press():
    for i,e in enumerate(Buttons):
        if not(e.value()):
            return i

e.send(str(-1))       # Send to all peers
newstate = -1
state = -1
while True:
    try:
      msg = b'%d' % newstate
      client.publish(topic_pub, msg)
    except OSError as e:
        restart_and_reconnect()
    sleep(0.1)
    state = on_press()
    if state != None:
        newstate = state
    try:
        new_message = client.check_msg()
    except OSError as e:
        restart_and_reconnect()
#     e.send(str(newstate))
   
