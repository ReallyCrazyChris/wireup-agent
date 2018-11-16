
import asyncio
import network
import socket
import ustruct

from config import nodekey, ip, port, multiaddr, ssid, passwd
from bencode import bencode, bdecode
from reactor import react
from queue import queue, receive, process

from store import Store #singelton
store = Store() #singelton

rt = {} #routing table


# join a wifi access point
# ssid string access point name
# passwd string accec point password
def joinwifi(ssid,passwd):
    
    # initiate a station mode
    _sta = network.WLAN(network.STA_IF)

    if not _sta.isconnected():
        print('connecting to network:', ssid)
        _sta.active(True)
        _sta.connect(ssid, passwd)

        while not _sta.isconnected():
            pass

    _ip = _sta.ifconfig()[0]
    print('connected as:', _ip)

    # deactivating access point mode
    _ap = network.WLAN(network.AP_IF)
    _ap.active(False)

def aton(ipv4address):
  a = []
  for i in ipv4address.split('.'):
    a.append(int(str(i)))
  return ustruct.pack('BBBB', a[0],a[1],a[2],a[3])

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
        await asyncio.sleep(1)
        print('receiveudpTask')
      
        try:
            msg, address = sock.recvfrom(1024) # Buffer size is 2048. Change as needed.
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


async def websocketTask ():
    while 1:
        await asyncio.sleep(1)
        print('websocketTask')
        process(react)


async def processTask ():
    while 1:
        await asyncio.sleep(1)
        print('processTask')

        
async def sendudpTask (sock):
    while 1:
        await asyncio.sleep(1)
        print('sendudpTask')   
        
        for toid in queue:

            packet = queue[toid]

            if (packet):
                msg = bencode(packet) 

                if toid == "all" : #  multicast
                    sock.sendto(msg, (multiaddr,port))

                elif toid == nodekey :
                    sock.sendto(msg, (ip,port))   

                elif (toid in rt)==True : #  unicast 
                    sock.sendto(msg, rt[toid])

                else:
                    print('destination unknown for', toid)
        
        queue.clear()


def listen():


    sock = getsocket()
    loop = asyncio.get_event_loop()

    loop.create_task( receiveudpTask(sock) )
    loop.create_task( websocketTask() )
    loop.create_task( processTask() )
    loop.create_task( sendudpTask(sock) )

    loop.run_forever()

if __name__ == "__main__":
    listen()