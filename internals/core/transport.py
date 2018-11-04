#!/usr/bin/env python
# encoding: utf-8
import socket
from config import ip, port, multiaddr
from actions import queue
from bencode import bencode, bdecode
from reactor import react
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

rt = {} # routing table

def listen(store):

    class WssHandler(WebSocket):

        def handleMessage(self):
            command, args = tuple( bdecode( self.data))
            print(args)
            react(command, args, store)
             
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
        for fileno in websocketserver.connections:
            connection = websocketserver.connections[fileno]
            msg = bencode(['update',store.toDict()])
            connection.sendMessage(msg)

    store.on('adddescription',lambda shadow,shadows: updateAllClients())        

    store.on('addshadow',lambda shadow,shadows: updateAllClients())

    store.on('removeshadow',lambda shadow,shadows: updateAllClients())

    store.on('shadowaddmodel',lambda shadow,model: updateAllClients())

    store.on('shadowremovemodel',lambda nodeid,modelid: updateAllClients())

    store.on('shadowaddwire',lambda shadow,shadows: updateAllClients())

    store.on('shadowremovewire',lambda shadow,shadows: updateAllClients())

    store.on('updateshadowmodel',lambda prop,value,shadowmodel: updateAllClients())

    print('wireup listening...')
    
    while True:
        receiveupd(store, s)
        sendudp(queue, s)
        websocketserver.serveonce()
            
def receiveupd(store, socket):

    try:
        msg, address = socket.recvfrom(4096) # Buffer size is 2048. Change as needed.
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

            while len(packets) > 1: 
                data = packets.pop()
                command = packets.pop()
                react(command, data, store)

def sendudp(queue, socket):

    for toid in queue:

        packet = queue[toid]

        if (packet):

            msg = bencode(packet) 

            if toid == "all" : #  multicast
                socket.sendto(msg, (multiaddr,port))

            elif (toid in rt)==True : #  unicast 
                socket.sendto(msg, rt[toid]) # TODO Error Handliong
            
            else:
                print('destination unknown for', toid)
        
    queue.clear()

