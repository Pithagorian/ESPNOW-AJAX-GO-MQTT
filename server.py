import network

from esp import espnow
from time import sleep
# A WLAN interface must be active to send()/recv()
wlan = network.WLAN(network.STA_IF)  # Or network.AP_IF
wlan.active(True)

e = espnow.ESPNow()
e.init()
'''
Dit is het mac address van de client het gegeven mac address is dat van de esp32 met knop
'''
peer = b'\x4c\xeb\xd6\x75\x53\xb4'   # MAC address of peer's wifi interface 
e.add_peer(peer)

e.send("Starting...")       # Send to all peers
for i in range(100):
    e.send(peer, str(i)*20, True)
    e.send(b'end')
    sleep(1)