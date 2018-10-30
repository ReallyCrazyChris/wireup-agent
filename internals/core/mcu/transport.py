#!/usr/bin/env python
# encoding: utf-8
import network
import socket
import ustruct
import time
from config import ssid, passwd
from bencode import bencode, bdecode

_port = 3300 #both udp and mulicast listen port
_multiaddr = '225.0.0.37' ## multicast addres

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

rt = {} # routing table
# Create a IPv4/UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    

def aton(ipv4address):
  a = []
  for i in ipv4address.split('.'):
    a.append(int(str(i)))
  return ustruct.pack('BBBB', a[0],a[1],a[2],a[3])

def listen(txqueue, react, store):
    # bind to the network adapter 
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0',_port))
    # register as a multicast listener
    mreq=aton(_multiaddr) + aton(_ip)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    s.setblocking(False)
    time.sleep(1)           # sleep for 1 second
    while True:
        receiveupd(react, store)
        sendudp(txqueue)

def receiveupd( react, store):
    try:
        msg, address = s.recvfrom(1024) # Buffer size is 2048. Change as needed.
    except:
        pass
    else:
        if msg:   

            packets = bdecode(msg)
            del msg
            
            if packets == False: return 

            to = packets.pop()    #  pop off to value
            fro = packets.pop()  #  pop off fro value

            if fro:
                rt[fro] = (address[0],address[1])  #  update routing table

            while len(packets) > 1: 
                data = packets.pop()
                command = packets.pop()
                react(command, data, to, fro, store)

def sendudp( txqueue ):

    for toid in txqueue:

        packet = txqueue[toid]

        if (packet):

            msg = bencode(packet) 
            
            del packet
            print('sending ',msg)

            if toid == "all" : #  multicast
                s.sendto(msg, (_multiaddr,_port))
            
            elif (toid in rt)==True : #  unicast 
                s.sendto(msg, rt[toid]) # TODO Error Handliong
            
            else:
                print('destination unknown for',toid)

            del msg
        
    txqueue.clear()
