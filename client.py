import network
from esp import espnow

# A WLAN interface must be active to send()/recv()
wlan= network.WLAN(network.STA_IF)
wlan.active(True)

e = espnow.ESPNow()
e.init()
'''
Dit is het macaddress van de client
'''
peer = b'\x4c\xeb\xd6\x75\x53\xb4'   # MAC address of peer's wifi interface
e.add_peer(peer)

while True:
    host, msg = e.irecv()     # Available on ESP32 and ESP8266
    if msg:             # msg == None if timeout in irecv()
        print(host, msg)
    
