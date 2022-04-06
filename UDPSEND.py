# UDP multicast for OBS by sendust
# Script is for OBS gane control


import socket
import sys
import struct
import msvcrt

port=50000
addr='239.192.1.100'
"""send(data[, port[, addr]]) - multicasts a UDP datagram."""
# Create the socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Make the socket multicast-aware, and set TTL.
s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20) # Change TTL (=20) to suit
s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
print("Make sure interest NIC is primary")
print(socket.gethostbyname_ex(socket.gethostname()))
# wait key input and send the data
while(1):
    print("Press number key (1~0)... '=' for exit")
    key = msvcrt.getch().decode("ASCII")
    print("You pressed " + key)
    s.sendto(bytes(key, "UTF-8"), (addr, port))
    if key == "=":
        break
s.close()
print("Finish script")
