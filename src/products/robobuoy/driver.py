import uasyncio as asyncio
from typecoersion import coerce
from machine import Pin

# initialize hardware (uncomment as needed)
#_active = Pin(0, Pin.IN)
#_steer = Pin(0, Pin.IN)
#_surge = Pin(0, Pin.IN)
#_minpwm = Pin(0, Pin.IN)
#_gain = Pin(0, Pin.IN)
#_maxpwm = Pin(0, Pin.IN)

def startdriver(product):
    """ initialize and start the hardware driver as a daemon """

    # listen for product events  (uncomment as needed)
    #product.on('active',lambda product, prop, value : 
        #_active.value(coerce(value, 'boolean')))
    #product.on('steer',lambda product, prop, value : 
        #_steer.value(coerce(value, 'integer')))
    #product.on('surge',lambda product, prop, value : 
        #_surge.value(coerce(value, 'integer')))
    #product.on('minpwm',lambda product, prop, value : 
        #_minpwm.value(coerce(value, 'integer')))
    #product.on('gain',lambda product, prop, value : 
        #_gain.value(coerce(value, 'integer')))
    #product.on('maxpwm',lambda product, prop, value : 
        #_maxpwm.value(coerce(value, 'integer')))

    # add a pollTask ot the event loop
    loop = asyncio.get_event_loop()
    loop.create_task(pollTask(product))


def stopdriver(product):
    """ stop and finalize the hardware driver """
    #_active.value(0)
    #_steer.value(0)
    #_surge.value(0)
    #_minpwm.value(0)
    #_gain.value(0)
    #_maxpwm.value(0)


async def pollTask(product):
    """ asyncronously poll the hardware and commmit data to the product model """
    while 1:
        await asyncio.sleep(0.1)
        """ commit _active input to product property active"""
        #product.commit('active',  _active.value())
        """ commit _steer input to product property steer"""
        #product.commit('steer',  _steer.value())
        """ commit _surge input to product property surge"""
        #product.commit('surge',  _surge.value())
        """ commit _minpwm input to product property minpwm"""
        #product.commit('minpwm',  _minpwm.value())
        """ commit _gain input to product property gain"""
        #product.commit('gain',  _gain.value())
        """ commit _maxpwm input to product property maxpwm"""
        #product.commit('maxpwm',  _maxpwm.value())
