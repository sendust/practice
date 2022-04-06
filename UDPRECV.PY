# UDP receiver for OBS gang control
# Created by sendust 2020/9/29
# Support Multiple OBS instance


import time
import socket
import struct
import win32gui
from pyautogui import hotkey


def windowenumerationhandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))


# Find title matching window and send key stroke


def winactive_sendhotkey(title, keystroke):
    top_windows = []
    win32gui.EnumWindows(windowenumerationhandler, top_windows)
    for i in top_windows:
        if title in i[1]:
            print(i)
            win32gui.ShowWindow(i[0], 5)
            time.sleep(0.1)
            win32gui.SetForegroundWindow(i[0])
            time.sleep(0.1)
            hotkey('ctrl', keystroke)


port = 50000
addr = "239.192.1.100"
buf_size = 1024
title_obs = "ONTACTCONCERT"

print("Make sure interest NIC is primary")
print(socket.gethostbyname_ex(socket.gethostname()))


# Create the socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set some options to make it multicast-friendly
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
except AttributeError:
    pass  # Some systems don't support SO_REUSEPORT
s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20)

# Bind to the port
s.bind(('', port))

# Set some more multicast options
intf = socket.gethostbyname(socket.gethostname())
s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(intf))
mreq = struct.pack("4sl", socket.inet_aton(addr), socket.INADDR_ANY)

s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


while 1:
    data, sender_addr = s.recvfrom(buf_size)
    cmd = data.decode("UTF-8")
    print("Received UDP command is " + cmd)
    if cmd == "1":
        winactive_sendhotkey(title_obs, "1")
    if cmd == "2":
        winactive_sendhotkey(title_obs, "2")
    if cmd == "3":
        winactive_sendhotkey(title_obs, "3")
    if cmd == "4":
        winactive_sendhotkey(title_obs, "4")
    if cmd == "5":
        winactive_sendhotkey(title_obs, "5")
    if cmd == "6":
        winactive_sendhotkey(title_obs, "6")
    if cmd == "7":
        winactive_sendhotkey(title_obs, "7")
    if cmd == "8":
        winactive_sendhotkey(title_obs, "8")
    if cmd == "9":
        winactive_sendhotkey(title_obs, "9")
    if cmd == "0":
        winactive_sendhotkey(title_obs, "0")
    if cmd == "F12":
        break

# unregister multicast receive membership, then close the port
s.setsockopt(socket.SOL_IP, socket.IP_DROP_MEMBERSHIP, socket.inet_aton(addr) + socket.inet_aton('0.0.0.0'))
s.close()
