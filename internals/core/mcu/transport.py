#!/usr/bin/env python
# encoding: utf-8
import network
import ustruct
import time
import socket
from config import ip, port, multiaddr, ssid, passwd
from actions import queue
from bencode import bencode, bdecode
from reactor import react

rt = {} # routing table

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

def aton(ipv4address):
  a = []
  for i in ipv4address.split('.'):
    a.append(int(str(i)))
  return ustruct.pack('BBBB', a[0],a[1],a[2],a[3])

def listen(store):

    # Create a IPv4/UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    
    # bind to the network adapter 
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0',port))
    # register as a multicast listener
    mreq=aton(multiaddr) + aton(_ip)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    s.setblocking(False)
    time.sleep(1)           # sleep for 1 second
    while True:
        receiveupd(store, s)
        sendudp(queue, s)

def receiveupd(store, socket):

    try:
        msg, address = socket.recvfrom(1024) # Buffer size is 2048. Change as needed.
    except: 
        # exceptions will be continoulsy thrown due to the non-blocking
        pass
    else:
        if msg:
           
            print('>-', msg)
            packets = bdecode(msg)
            
            if packets == False: return 

            #print(packets)

            to = packets.pop()    #  pop off to value
            fro = packets.pop()  #  pop off fro value

            if fro:
                rt[fro] = (address[0],address[1])  #  update routing table

            while len(packets) > 1: 
                data = packets.pop()
                command = packets.pop()
                react(command, data, store)

def sendudp(queue, socket):

    for toid in queue:

        packet = queue[toid]

        if (packet):

            msg = bencode(packet) 
            print('->', msg)
            if toid == "all" : #  multicast
                socket.sendto(msg, (multiaddr,port))

            elif (toid in rt)==True : #  unicast 
                socket.sendto(msg, rt[toid]) # TODO Error Handliong
            
            else:
                print('destination unknown for', toid)
        
    queue.clear()

