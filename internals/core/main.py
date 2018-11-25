try:
    import asyncio
    from wstransport import getwebsocket            
except (ModuleNotFoundError, ImportError):
    import uasyncio as asyncio   
    from wifi import joinwifi    
  

from config import ip
from product import Product
from reactor import addmodel, announce, react
from udptransport import getsocket, receiveudp, sendudp


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

product = Product()
addmodel(product)
announce('','','')
listen()