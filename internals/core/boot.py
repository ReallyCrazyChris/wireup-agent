#!/usr/bin/env python
# encoding: utf-8
import network
from config import ssid, passwd

# initiate a station
_sta = network.WLAN(network.STA_IF)

if not _sta.isconnected():
    print('connecting to network...', ssid)
    _sta.active(True)
    # sta.connect('SummerTime', 'Calmhat436')
    _sta.connect(ssid, passwd)

    while not _sta.isconnected():
        pass

_ip = _sta.ifconfig()[0]
print('connected as:', _ip)

# close down the access point
_ap = network.WLAN(network.AP_IF)
_ap.active(False)
