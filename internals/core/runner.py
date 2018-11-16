
import asyncio
import socket
from config import nodekey, ip, port, multiaddr

rt = {} #routing table

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
            msg, address = sock.recvfrom(4096) # Buffer size is 2048. Change as needed.
        except Exception as e: 
            # exceptions will be continoulsy thrown due to the non-blocking
            print(e)
            pass
        else:
            if msg:
                print(msg)
                
                """
                packets = bdecode(msg)

                if packets == False: return

                to = packets.pop()   #  pop off to value
                fro = packets.pop()  #  pop off fro value

                if fro:
                    rt[fro] = (address[0],address[1])  #  update routing table

                print('receiveupd', packets)

                while len(packets): # TODO better bad packedt detection
                    receive(packets.pop())
                """


async def websocketTask ():
    while 1:
        await asyncio.sleep(1)
        print('websocketTask')
        
async def sendudpTask ():
    while 1:
        await asyncio.sleep(1)
        print('sendudpTask')   

def listen():

    sock = getsocket()
    loop = asyncio.get_event_loop()

    loop.create_task( receiveudpTask(sock) )
    loop.create_task( websocketTask() )
    loop.create_task( sendudpTask() )

    loop.run_forever()

if __name__ == "__main__":
    listen()