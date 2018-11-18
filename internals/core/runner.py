try:
    import uasyncio as asyncio                    
except ImportError:
    import asyncio
  
from udptransport import getsocket, receiveudp, sendudp
from wstransport import getwebsocket
from reactor import react

async def receiveudpTask(sock):
    while 1:
        await asyncio.sleep(0)
        receiveudp(sock)
        sendudp(sock)

async def reactTask():
    while 1:
        await asyncio.sleep(0)
        react()

async def sendudpTask(sock):
    while 1:
        await asyncio.sleep(0)
        sendudp(sock)

async def websocketTask(websock):
    while 1:
        await asyncio.sleep(0)
        websock.serveonce()

def listen():

    sock = getsocket()
    websock = getwebsocket()

    print('moop')

    loop = asyncio.get_event_loop()

    #loop.create_task( receiveudpTask(sock) )
    loop.create_task( websocketTask(websock) )
    #loop.create_task( reactTask() )
    #loop.create_task( sendudpTask(sock) )

    loop.run_forever()

if __name__ == "__main__":
    listen()