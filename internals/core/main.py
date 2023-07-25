from reactor import addmodel, announce, react
from config import ip

try:

    from wstransport import getwebsocket
    import asyncio
    import socket

    # detect the ip address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
         # doesn't even have to be reachable
         s.connect(('10.255.255.255', 1))
         ip = s.getsockname()[0]
    except:
         ip = '127.0.0.1'
    finally:
         s.close()

except (ImportError):
    import uasyncio as asyncio
    from wifi import joinwifi


from product import Product
from udptransport import getsocket, receiveudp, sendudp


async def reactTask(sock):
    while 1:
        receiveudp(sock)
        react()
        sendudp(sock)
        await asyncio.sleep(0)

async def websockTask(websock):
    while 1:
        websock.serveonce()
        await asyncio.sleep(0)

async def heartbeatTask():
    while 1:
        await asyncio.sleep(10)
        announce('','','')

async def main_task():

    try:# to create a websocket
        websock = getwebsocket()
        asyncio.create_task( websockTask(websock) )
    except Exception:
        pass

    try:# to join a wfinetwork (micropython)
        sock = getsocket(joinwifi())
        asyncio.create_task( reactTask(sock) )
        asyncio.create_task( heartbeatTask() )
    except Exception:
        #cpython approach
        sock = getsocket(ip)
        asyncio.create_task( reactTask(sock) )
        asyncio.create_task( heartbeatTask() )

    while 1:
        await asyncio.sleep(60)
        print('still alive')

if __name__ == "__main__":

        print('WireUp Agent v0.1')
        product = Product()
        addmodel(product)
        asyncio.run( main_task() )

