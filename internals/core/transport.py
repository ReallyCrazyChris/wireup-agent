#!/usr/bin/env python
# encoding: utf-8
import socket
from config import nodekey, ip, port, multiaddr
from bencode import bencode, bdecode
from reactor import react
from queue import queue, receive, process

from store import Store
store = Store()

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

rt = {} #routing table

def listen():

    class WssHandler(WebSocket):

        def handleMessage(self):
            msg = bdecode( self.data )
            receive(msg)
             
        def handleConnected(self):
            print(self.address, 'connected')
            msg = bencode(['update',store.toDict()])
            self.sendMessage(msg)

        def handleClose(self):
            print(self.address, 'closed')

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # Create a IPv4/UDP socket  
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Reuse the network adapter for other protocols
    s.bind((ip,port))     # Bind to a network adapter on a port
    mreq=socket.inet_aton(multiaddr)+socket.inet_aton(ip) # calcualte the multicast receiver enrt
    s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)    # Register as a muticast receiver 
    s.setblocking(False)
    
    websocketserver = SimpleWebSocketServer(ip, 9090, WssHandler)

    def updateAllClients():
        print('updateAllClients')
        for fileno in websocketserver.connections:
            connection = websocketserver.connections[fileno]
            msg = bencode(['update',store.toDict()])
            connection.sendMessage(msg)

    store.on('adddescription',lambda shadow,shadows: updateAllClients())        

    store.on('addshadow',lambda shadow,shadows: updateAllClients())

    store.on('removeshadow',lambda shadow,shadows: updateAllClients())

    store.on('shadowaddmodel',lambda shadow,model: updateAllClients())

    store.on('shadowremovemodel',lambda nodeid,modelid: updateAllClients())

    store.on('shadowaddwire',lambda producer,consumer: updateAllClients())

    store.on('shadowremovewire',lambda producer,consumer: updateAllClients())
    
    store.on('updateshadowmodel',lambda prop,value,shadowmodel: updateAllClients())
    
    while True:
        process(react)
        websocketserver.serveonce()
        receiveupd(s)  
        sendudp(queue, s)
        
def receiveupd(socket):

    try:
        msg, address = socket.recvfrom(4096) # Buffer size is 2048. Change as needed.
    except: 
        # exceptions will be continoulsy thrown due to the non-blocking
        pass
    else:
        if msg:
            packets = bdecode(msg)

            if packets == False: return

            to = packets.pop()   #  pop off to value
            fro = packets.pop()  #  pop off fro value

            if fro:
                rt[fro] = (address[0],address[1])  #  update routing table

            print('receiveupd', packets)

            while len(packets): # TODO better bad packedt detection
                receive(packets.pop())

def sendudp(queue, socket):

    for toid in queue:

        packet = queue[toid]

        if (packet):

            print('sendudp', packet)
            msg = bencode(packet)
             
            if toid == "all": #multicast
                socket.sendto(msg, (multiaddr,port))

            elif toid == nodekey :
                socket.sendto(msg, (ip,port))

            elif (toid in rt) == True : #  unicast 
                socket.sendto(msg, rt[toid]) # TODO Error Handliong

            else:
                print('destination unknown for', toid)
        
    queue.clear()
