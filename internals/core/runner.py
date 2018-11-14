
import asyncio
import socket
from config import nodekey, ip, port, multiaddr
from bencode import bencode, bdecode

def datagramsocket():
    ## create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # Create a IPv4/UDP socket  
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Reuse the network adapter for other protocols
    s.bind((ip,port))     # Bind to a network adapter on a port
    ## register at the router as a multicast listener
    mreq=socket.inet_aton(multiaddr)+socket.inet_aton(ip) # calcualte the multicast receiver enrt
    s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)    # Register as a muticast receiver 
    s.setblocking(False)
    return s

async def datgramsend(data,addr):
    socket.sendto('hello world', (ip,port))


async def datagramreceive():
    global sock
    while 1:
        try:
            data, address = sock.recvfrom(4096) # Buffer size is 2048. Change as needed.
            print('got data',data,address)
            await asyncio.sleep(1)  # Pause 1s
        except: 
            print('oops')
            await asyncio.sleep(1)  # Pause 1s


async def killer():
    await asyncio.sleep(10)  

sock = datagramsocket()
loop = asyncio.get_event_loop()

try:
    loop.create_task(datagramreceive())
    loop.run_until_complete(killer())
except KeyboardInterrupt as e:
    print("Caught keyboard interrupt.") 
finally:
    loop.close()
