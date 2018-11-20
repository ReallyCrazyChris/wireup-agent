try:
    import asyncio            
except ImportError:
    import uasyncio as asyncio   
    from wifi import joinwifi    
  
from udptransport import getsocket, receiveudp, sendudp
from wstransport import getwebsocket
from reactor import react
from config import ip

async def mainTask(sock):
    while 1:
        receiveudp(sock)
        react()
        sendudp(sock)
        await asyncio.sleep(0)

async def websockTask():
    websock = getwebsocket()
    while 1:
        websock.serveonce()
        await asyncio.sleep(0)

def listen():

    try:#micropython approach
        sock = getsocket(joinwifi())
    except Exception:
        #cpython approach
        sock = getsocket(ip)

    loop = asyncio.get_event_loop()
    loop.create_task( mainTask(sock) )
    loop.create_task( websockTask() )
    loop.run_forever()
