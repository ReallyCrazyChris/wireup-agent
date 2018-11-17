try:
    import uasyncio as asyncio                    
except ImportError:
    import asyncio

import socket
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

from config import nodekey, ip, port, multiaddr
from bencode import bencode, bdecode
from reactor import react
from queue import queue, receive, process

from store import Store #singelton
store = Store() #singelton

rt = {} #routing table

def getwebsocket(store):

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


    def updateAllClients(websocketserver,store):
        print('updateAllClients')
        for fileno in websocketserver.connections:
            connection = websocketserver.connections[fileno]
            msg = bencode(['update',store.toDict()])
            connection.sendMessage(msg)

    websocketserver = SimpleWebSocketServer(ip, 9090, WssHandler)   

    # register for all store events
    store.on('*',lambda *args: updateAllClients(websocketserver,store))  

    return websocketserver


def getsocket():
    # bind to a network adapter on ip and port
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # Create a IPv4/UDP socket  
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Reuse the network adapter for other protocols
    s.bind((ip,port))     # Bind to a network adapter on port
    
    # register as a multicast listener with the router.
    mreq=socket.inet_aton(multiaddr)+socket.inet_aton(ip) # calcualte the multicast receiver enrt
    s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)    # Register as a muticast receiver 
    s.setblocking(False)

    return s

async def receiveudpTask (sock):
    while 1:
        await asyncio.sleep(0)
        
        try:
            msg, address = sock.recvfrom(4096) # Buffer size is 2048. Change as needed.
        except: 
            # exceptions will be continoulsy thrown due to the non-blocking of recivefrom
            pass
        else:
            if msg:
                print(msg)
                packets = bdecode(msg)
                if packets == False: return 
                #print(packets)
                to = packets.pop()    #  pop off to value
                fro = packets.pop()  #  pop off fro value

                if fro:
                    rt[fro] = (address[0],address[1])  # update the routing table

                while len(packets): # TODO better bad packedt detection
                    receive(packets.pop())

async def websocketTask (websock):
    while 1:
        await asyncio.sleep(0)
        websock.serveonce()
    

async def processTask ():
    while 1:
        await asyncio.sleep(0)
        process(react)

# encodes and sends grouped packets to a destination       
async def sendudpTask (sock):
    while 1:
        await asyncio.sleep(0)
        
        for toid in queue:

            packet = queue[toid]

            if (packet):
                msg = bencode(packet) 

                if toid == "all" : #  multicast
                    sock.sendto(msg, (multiaddr,port))

                elif toid == nodekey : # internal comm
                    sock.sendto(msg, (ip,port))   

                elif (toid in rt)==True : #  unicast 
                    sock.sendto(msg, rt[toid])

                else:
                    print('destination unknown for', toid)
        
        queue.clear()

def listen():

    sock = getsocket()
    websock = getwebsocket(store)
    loop = asyncio.get_event_loop()

    loop.create_task( receiveudpTask(sock) )
    loop.create_task( websocketTask(websock) )
    loop.create_task( processTask() )
    loop.create_task( sendudpTask(sock) )

    loop.run_forever()

if __name__ == "__main__":
    listen()