#!/usr/bin/env python
# encoding: utf-8
import network
import ustruct
import time

import socket
from config import nodekey, ip, port, multiaddr
from bencode import bencode, bdecode
from reactor import react
from queue import queue, receive, process

from store import Store
store = Store()

# initiate a station
_sta = network.WLAN(network.STA_IF)

if not _sta.isconnected():
    print('connecting to network...', ssid)
    _sta.active(True)
    _sta.connect(ssid, passwd)

    while not _sta.isconnected():
        pass

_ip = _sta.ifconfig()[0]
print('connected as:', _ip)

# close down the access point
_ap = network.WLAN(network.AP_IF)
_ap.active(False)

def aton(ipv4address):
  a = []
  for i in ipv4address.split('.'):
    a.append(int(str(i)))
  return ustruct.pack('BBBB', a[0],a[1],a[2],a[3])

rt = {} # routing table

def listen():

    # Create a IPv4/UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    
    # bind to the network adapter 
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip,port))
    # register as a multicast listener
    mreq=aton(multiaddr) + aton(_ip)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    s.setblocking(False)
    time.sleep(1)           # sleep for 1 second
    while True:
        receiveupd(store, s)
        sendudp(queue, s)

def receiveupd(socket):

    try:
        msg, address = socket.recvfrom(1024) # Buffer size is 2048. Change as needed.
    except: 
        # exceptions will be continoulsy thrown due to the non-blocking
        pass
    else:
        if msg:

            packets = bdecode(msg)
            if packets == False: return 
            #print(packets)
            to = packets.pop()    #  pop off to value
            fro = packets.pop()  #  pop off fro value

            if fro:
                rt[fro] = (address[0],address[1])  #  update routing table

            while len(packets): # TODO better bad packedt detection
                receive(packets.pop())

def sendudp(queue, socket):

    for toid in queue:

        packet = queue[toid]

        if (packet):
            msg = bencode(packet) 

            if toid == "all" : #  multicast
                socket.sendto(msg, (multiaddr,port))

            elif toid == nodekey :
                socket.sendto(msg, (ip,port))   

            elif (toid in rt)==True : #  unicast 
                socket.sendto(msg, rt[toid])

            else:
                print('destination unknown for', toid)
        
    queue.clear()
