import uasyncio as asyncio
from typecoersion import coerce
from machine import Pin

# initialize hardware (uncomment as needed)
_push = Pin(4, Pin.IN)
_sayilike = Pin(2, Pin.OUT)

def startdriver(product):
    """ initialize and start the hardware driver as a daemon """

    # listen for product events  (uncomment as needed)
    #self.on('push',lambda product, prop, value : 
        #_push.value(coerce(value, 'boolean')))
    product.on('sayilike',lambda product, prop, value : 
        _sayilike.value(coerce(value, 'integer')))

    # add a pollTask ot the event loop
    loop = asyncio.get_event_loop()
    loop.create_task(pollTask(product))


def stopdriver(product):
    """ stop and finalize the hardware driver """
    #_push.value(0)
    #_sayilike.value(0)


async def pollTask(product):
    """ asyncronously poll the hardware and commmit data to the product model """
    while 1:
        await asyncio.sleep(0.1)
        """ commit _push input to product property push"""
        product.commit('push',  _push.value())
        """ commit _sayilike input to product property sayilike"""
        #product.commit('sayilike',  _sayilike.value())
