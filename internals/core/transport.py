#!/usr/bin/env python
# encoding: utf-8

import socket
from bencode import bencode, bdecode
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

#ip = '0.0.0.0' # address of the network adapter to use
ip='192.168.2.107'
port = 3300 #both udp and mulicast listen port
multiaddr = '225.0.0.37' ## multicast addres

rt = {} # routing table

# Create a IPv4/UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)    
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind to a Port
s.bind((ip,port))

# Register as a muticast receiver 
mreq=socket.inet_aton(multiaddr)+socket.inet_aton(ip)
s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

s.setblocking(False)

def listen(txqueue, react, store):

    class WssHandler(WebSocket):

        def handleMessage(self):
            command, args = tuple( bdecode( self.data))
            react( command, args, '', '', store )
             
        def handleConnected(self):
            print(self.address, 'connected')
            msg = bencode(['update',store.toDict()])
            self.sendMessage(msg)

        def handleClose(self):
            print(self.address, 'closed')

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
        receiveupd( react, store)
        sendudp( txqueue )
        websocketserver.serveonce()
            
def receiveupd( react, store):

    try:
        msg, address = s.recvfrom(2048) # Buffer size is 2048. Change as needed.
    except: 
        # exceptions will be continoulsy thrown due to the non-blocking
        pass
    else:
        if msg:
           
           
            packets = bdecode(msg)
            
            if packets == False: return 

            print(packets)

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

            if toid == "all" : #  multicast
                s.sendto(msg, (multiaddr,port))

            elif (toid in rt)==True : #  unicast 
                s.sendto(msg, rt[toid]) # TODO Error Handliong
            
            else:
                print('destination unknown for',toid)
        
    txqueue.clear()
