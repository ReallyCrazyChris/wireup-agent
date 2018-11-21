try:
    import asyncio
    from wstransport import getwebsocket            
except ImportError:
    import uasyncio as asyncio   
    from wifi import joinwifi    
  
from udptransport import getsocket, receiveudp, sendudp

from reactor import react
from config import ip

async def mainTask(sock):
    while 1:
        receiveudp(sock)
        react()
        sendudp(sock)
        await asyncio.sleep(0)

async def websockTask(websock):
    while 1:
        websock.serveonce()
        await asyncio.sleep(0)

def listen():

    loop = asyncio.get_event_loop()

    try:# to join a wfinetwork (micropython)
        sock = getsocket(joinwifi())
        loop.create_task( mainTask(sock) )  
    except Exception:
        #cpython approach
        sock = getsocket(ip)
        loop.create_task( mainTask(sock) )  

    try:# to create a websocket
        websock = getwebsocket()
        loop.create_task( websockTask(websock) )
    except Exception:
        pass

    loop.run_forever()
