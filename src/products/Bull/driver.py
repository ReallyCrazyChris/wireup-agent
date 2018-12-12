import uasyncio as asyncio
from typecoersion import coerce
from machine import Pin

# initialize hardware (uncomment as needed)
_push = Pin(0, Pin.IN)
_saybull = Pin(0, Pin.OUT)
_led = Pin(0, Pin.OUT)

def startdriver(product):
    """ initialize and start the hardware driver as a daemon """

    # listen for product events  (uncomment as needed)
    #product.on('push',lambda product, prop, value : 
        #_push.value(coerce(value, 'boolean')))
    product.on('saybull',lambda product, prop, value : 
        _saybull.value(coerce(value, 'boolean')))
    product.on('led',lambda product, prop, value : 
        _led.value(coerce(value, 'boolean')))

    # add a pollTask ot the event loop
    loop = asyncio.get_event_loop()
    loop.create_task(pollTask(product))


def stopdriver(product):
    """ stop and finalize the hardware driver """
    #_push.value(0)
    #_saybull.value(0)
    #_led.value(0)


async def pollTask(product):
    """ asyncronously poll the hardware and commmit data to the product model """
    while 1:
        await asyncio.sleep(0.1)
        """ commit _push input to product property push"""
        product.commit('push',  _push.value())
        """ commit _saybull input to product property saybull"""
        #product.commit('saybull',  _saybull.value())
        """ commit _led input to product property led"""
        #product.commit('led',  _led.value())
