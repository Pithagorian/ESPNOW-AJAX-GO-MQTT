import network

from esp import espnow
from time import sleep
# A WLAN interface must be active to send()/recv()
wlan = network.WLAN(network.STA_IF)  # Or network.AP_IF
wlan.active(True)

e = espnow.ESPNow()
e.init()
peer = b'\x1a\x2b\x3c\x4d\x5e\x6f'   # MAC address of client's wifi interface 
e.add_peer(peer)

e.send("Starting...")       # Send to all peers
for i in range(100):
    e.send(peer, str(i)*20, True)
    e.send(b'end')
    sleep(1)
