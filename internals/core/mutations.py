#import importlib
from config import nodekey
from typecoersion import coerce
from reactor import send

from store import Store
store = Store()  # singelton


def announce(product,to=0):
    send(nodekey, to, 'ad', product.toDescription())


def addmodel(model):
    """adds a Model instance to the store"""
    if (model.id in store.models) == True:
        return  # model exists

    if model.id == False:  # provide an id if the model has none
        store.pointer += 1
    model.id = str(store.pointer)  # model.id is a string
    model.nodeid = store.nodeid  # provide the model with a nodeid

    store.models[model.id] = model

    model.start()  # lifecycle start

    for shadowlistenerid in store.shadowlisteners:  # propagate to shadow listeners
        send(nodekey, shadowlistenerid, 'sam', model.toDict())


def removemodel(modelid):
    if (modelid in store.models) == False:
        return  # model does'nt exists
    model = store.models[modelid]
    model.stop()

    for shadowlistenerid in store.shadowlisteners:  # propagate to shadow listeners
        send(nodekey, shadowlistenerid, 'srm', model.nodeid, model.id)

    del store.models[modelid]


def addbrick(brickname):
    """not yet implemented"""
    #brickinstance = importlib.import_module('bricks.'+str( brickname ) ).Brick()
    # addmodel(brickinstance)
    pass


def updatemodel(modelid, prop, value, salt=None):
    """ updates a property value, notifies shadow listeners and wire listeners """
    if (modelid in store.models) == False:
        return  # unknowm model
    model = store.models[modelid]
    if (prop in model.props) == False:
        return  # unknown prop

    # TODO reduce the size of the salt
    if salt == model.nodeid+modelid+prop:
        return  # circular race condition detected
    # detect future reace condition by setting salt
    salt = salt or model.nodeid+modelid+prop

    proptype = model.meta[prop]['type']

    # coerces the value to the property type
    coercedvalue = coerce(value, proptype)

    if model.props[prop] == coercedvalue:
        return  # no change to the value

    model.props[prop] = coercedvalue  # assigns the new value

    # emit a property value change event
    model.emit(prop, model, prop, model.props[prop])

    # propagate to shadow models
    for shadownodeid in store.shadowlisteners:
        send(nodekey, shadownodeid, 'udsm', model.nodeid, model.id, prop, coercedvalue)

    if (prop in model.wires) == False:
        return  # any wire listeners for prop

    wirelisteners = model.wires[prop]
    # propagate the value to the wire listeners
    for listeneruri in wirelisteners:
        listenernodeid, listnermodlid, listenerprop = tuple(
            listeneruri.split('/'))
        send(nodekey, listenernodeid, 'udm', listenernodeid,
             listnermodlid, listenerprop, coercedvalue, salt)


def addwirelistener(producer, consumer):
    """add wire listener, to be notified when a model property changes, updates/notifies shadow listeners"""

    pnodeid, pmodelid, pprop = tuple(producer.split('/'))
    cnodeid, cmodelid, cprop = tuple(consumer.split('/'))

    if (pmodelid in store.models) == False:
        return  # no such model

    model = store.models[pmodelid]

    if (pprop in model.props) == False:
        return  # no such key

    if (pprop in model.wires) == False:  # cretae a dict for the prop if there is none
        model.wires[pprop] = {}

    if (pprop in model.wires) == True:
        model.wires[pprop][consumer] = ''

    for shadowlistenerid in store.shadowlisteners:  # propagate to shadow listeners
        send(nodekey, shadowlistenerid, 'sawl', producer, consumer)

    # propagate the value to the property listener
    send(nodekey, cnodeid, 'udm', cnodeid, cmodelid, cprop, model.props[pprop])

    # save the store state to non-volatile memory, so the wire state is remembered
    store.serialize()


def removewirelistener(producer, consumer):
    """removes wire listener, updates/notifies shadow listeners"""
    pnodeid, pmodelid, pprop = tuple(producer.split('/'))
    # cnodeid,cmodelid,cprop = tuple(consumer.split('/'))

    if (pmodelid in store.models) == False:
        return  # no such model

    model = store.models[pmodelid]

    if (pprop in model.props) == False:
        return  # no such key

    if (pprop in model.wires) == False:
        return  # no such wire

    if (pprop in model.wires) == True:
        if (consumer in model.wires[pprop]) == True:
            del model.wires[pprop][consumer]

    for shadowlistenerid in store.shadowlisteners:  # propagate to shadow listeners
        send(nodekey, shadowlistenerid, 'srwl', producer, consumer)

    # save the store state to non-volatile memory, so the wire state is remembered
    store.serialize()


def addshadowlistener(listenernodeid):
    """request to a remote node, so add self as a shadow listener"""
    # register the shadow listener
    store.shadowlisteners[listenernodeid] = True
    models = {}
    for modelid in store.models:
        models[modelid] = (store.models[modelid]).toDict()
    # notify the listener the current models
    send(nodekey, listenernodeid, 'ash', store.nodeid, models)


def removeshadowlistener(listenernodeid):
    """request to a remote node, so remove self as a shadow listener"""
    if listenernodeid in store.shadowlisteners:
        # unregister the shadow listener
        del store.shadowlisteners[listenernodeid]
        # notify the listener the current models
        send(nodekey, 'rsh', [store.nodeid], listenernodeid)


""" from here on master node only """


def adddescription(nodeid, description):
    """add descrption, of a discovered Product"""
    store.discovered[nodeid] = description
    store.emit('adddescription', description, nodeid)


def addshadow(nodeid, shadow):
    """adds a shadow of a node, emits an event"""
    store.shadows[nodeid] = shadow          # register the shadowin shadows
    # shadow emits a shadow and shadows
    store.emit('addshadow', shadow, store.shadows)


def removeshadow(shadownodeid):
    """removes a shadow of a node, emits an event"""
    del store.shadows[shadownodeid]  # unregister the shadowin shadows
    # shadow emits a shadow and shadows
    store.emit('removeshadow', shadownodeid, store.shadows)


def updateshadowmodel(nodeid, modelid, prop, value):
    """notifies shadow listeners of an model property change"""
    if (nodeid in store.shadows) == False:
        return  # unknown shadow
    shadow = store.shadows[nodeid]
    if (modelid in shadow) == False:
        return  # unknow shadowmodel
    shadowmodel = shadow[modelid]

    # update the value #TODO Check that the reference structure is correct
    shadowmodel['props'][prop] = value

    # shadow emits a key, value ,model
    store.emit('updateshadowmodel', prop, value, shadowmodel)


def shadowaddwirelistener(producer, consumer):
    """shadow add wire listener, updates shadow state from orign model state"""
    nodeid, modelid, prop = tuple(producer.split('/'))

    if (nodeid in store.shadows) == False:
        return  # no such shadow

    shadow = store.shadows[nodeid]

    if (modelid in shadow) == False:
        return  # no such shadowmodel

    shadowmodel = shadow[modelid]

    if (prop in shadowmodel['props']) == False:
        return  # no such property

    # create a wire disctioniary if needed
    if (prop in shadowmodel['wires']) == False:
        shadowmodel['wires'][prop] = {}

    if (prop in shadowmodel['wires']) == True:
        # create a wire to the consumer
        shadowmodel['wires'][prop][consumer] = ''

    store.emit('shadowaddwire', producer, consumer)


def shadowremovewirelistener(producer, consumer):
    """shadow remove wire listener, updates shadow state from orign model state"""
    nodeid, modelid, prop = tuple(producer.split('/'))

    if (nodeid in store.shadows) == False:
        return  # no such shadow

    shadow = store.shadows[nodeid]

    if (modelid in shadow) == False:
        return  # no such shadowmodel

    shadowmodel = shadow[modelid]

    if (prop in shadowmodel['wires']) == False:
        return  # no such proprty

    if (consumer in shadowmodel['wires'][prop]) == False:
        return

    del shadowmodel['wires'][prop][consumer]  # remove wire to the consumer

    store.emit('shadowremovewire', producer, consumer)


def shadowaddmodel(model):
    """shadow add model, updates shadow state from orign model state"""
    nodeid = model['nodeid']
    modelid = model['id']

    if (nodeid in store.shadows) == False:
        return  # no such shadow

    shadow = store.shadows[nodeid]

    shadow[modelid] = model  # assign the shadowmodel

    store.emit('shadowaddmodel', shadow, model)


def shadowremovemodel(nodeid, modelid):
    """shadow remove model, updates shadow state from orign model state"""
    if (nodeid in store.shadows) == False:
        return  # no such shadow

    shadow = store.shadows[nodeid]

    if (modelid in shadow) == False:
        return  # no such shadowmodel

    del store.shadows[nodeid][modelid]  # delete the shadow model

    store.emit('shadowremovemodel', nodeid, modelid)
