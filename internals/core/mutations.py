import importlib
from typecoersion import coerce
from queue import send

#addmodel - adds a Model instance to the store
# @param store refence to store
# @param model subclass object of Model
def addmodel(store,model):

    if (model.id in store.models) == True: return # model exists
      
    if model.id == False: # provide an id if the model has none
       store.pointer +=1
    model.id = str(store.pointer)        #model.id is a string
    model.nodeid = store.nodeid  # provide the model with a nodeid
    
    store.models[model.id] = model

    model.start(store) # lifecycle start

    for shadowlistenerid in store.shadowlisteners: # propagate to shadow listeners
      send('sam',[model.toDict()],shadowlistenerid)

def removemodel(store,modelid):
    if (modelid in store.models) == False: return # model does'nt exists  
    model = store.models[modelid]
    model.stop(store)

    for shadowlistenerid in store.shadowlisteners: # propagate to shadow listeners
      send('srm',[model.nodeid,model.id],shadowlistenerid)

    del store.models[modelid]
 
def addbrick(store, brickname):
    brickinstance = importlib.import_module('bricks.'+str( brickname ) ).Brick()
    addmodel(store, brickinstance)

## updatemodel update model
# @param modelid integer
# @param prop string
# @param value any
# @param s store reference
def updatemodel( store,nodeid,modelid,prop,value ):

    if (modelid in store.models)==False: return # unknowm model

    model = store.models[modelid]

    proptype = model.meta[prop]['type']

    coercedvalue = coerce(value,proptype) # coerces the value to the property type

    if model.props[prop] == coercedvalue: return # no value change

    model.props[prop] = coercedvalue # assigns the new value

    model.emit(prop, store, prop, model.props[prop]) # emit a property value change event

    # propagate to shadow models
    for shadownodeid in store.shadowlisteners:
      send('udsm',[nodeid,modelid,prop,coercedvalue],shadownodeid)
          
    if (prop in model.wires)==False: return # any wire listeners for prop      
    
    wirelisteners = model.wires[prop]
    # propagate the value to the wire listeners
    for listeneruri in wirelisteners:
      listenernodeid,listnermodlid,listenerprop = tuple(listeneruri.split('/'))
      send('udm',[listenernodeid,listnermodlid,listenerprop,coercedvalue],listenernodeid)

## add wire listener, to be nitified when a model property changes
# producer string uri of the producer property
# consumer string uri of the consumer property
def addwirelistener( store,producer,consumer):

    pnodeid,pmodelid,pprop = tuple(producer.split('/'))
    cnodeid,cmodelid,cprop = tuple(consumer.split('/'))

    if (pmodelid in store.models)==False: return # no such model

    model = store.models[pmodelid]  

    if (pprop in model.props)==False: return # no such key  

    if (pprop in model.wires)==False: # cretae a dict for the prop if there is none
      model.wires[pprop] = {}

    if (pprop in model.wires)==True:
      model.wires[pprop][consumer] = ''

    for shadowlistenerid in store.shadowlisteners: # propagate to shadow listeners
      send('sawl',[producer,consumer],shadowlistenerid)  

    send('udm',[cnodeid,cmodelid,cprop,model.props[pprop]],cnodeid)   # propagate the value to the property listener

    # save the store state to non-volatile memory, so the wire state is remembered
    store.serialize()

## remove wire listener
# producer string uri of the producer property
# consumer string uri of the consumer property
def removewirelistener( store,producer,consumer ):

    pnodeid,pmodelid,pprop = tuple(producer.split('/'))
    # cnodeid,cmodelid,cprop = tuple(consumer.split('/'))

    if (pmodelid in store.models)==False: return # no such model

    model = store.models[pmodelid]  

    if (pprop in model.props)==False: return # no such key  

    if (pprop in model.wires)==False: return # no such wire

    if (pprop in model.wires)==True:
      if (consumer in model.wires[pprop])==True:
        del model.wires[pprop][consumer]

    for shadowlistenerid in store.shadowlisteners: # propagate to shadow listeners
      send('srwl',[producer,consumer],shadowlistenerid)  

    # save the store state to non-volatile memory, so the wire state is remembered
    store.serialize()

## add shadow listener, to be notified when a model updates 
# listenerdata table shadoe lisener nodeid
# shadowlisteners table
# models table
def addshadowlistener( store,listenernodeid ):
    store.shadowlisteners[listenernodeid] = True # register the shadow listener
    models = {}
    for modelid in store.models:
      models[modelid] = (store.models[modelid]).toDict()    
    send('ash',[store.nodeid,models],listenernodeid) # notify the listener the current models

## removeshadowlistener
# listenerdata table shadoe lisener nodeid
# shadowlisteners table
# models table
def removeshadowlistener( store,listenernodeid ):
    if listenernodeid in store.shadowlisteners:
        del store.shadowlisteners[listenernodeid] # unregister the shadow listener
        send('rsh',[store.nodeid],listenernodeid) # notify the listener the current models


""" from here on master node only """

## add descrption, of a discovered Product 
# @param descritpion dictionary decribing a Product
# @param nodeid nodekey of the Product
def adddescription(store, description,nodeid):  
    store.discovered[nodeid] = description
    store.emit('adddescription',description,nodeid)

## add shadow of a Product
# @param nodeid string identifier of the Product being shadowed
# @param shadow dict of the shadowed Product
def addshadow( store,nodeid, shadow ):
    store.shadows[nodeid] = shadow          # register the shadowin shadows
    store.emit('addshadow',shadow,store.shadows) # shadow emits a shadow and shadows

## remove shadow of a Product
# @param shadownodeid string Product identifier
def removeshadow( store,shadownodeid ):
    del store.shadows[shadownodeid]  # unregister the shadowin shadows
    store.emit('removeshadow',shadownodeid,store.shadows) # shadow emits a shadow and shadows
  
## update shadow model
# @param nodeid string
# @param modelid number
# @param prop string
# @param value any
def updateshadowmodel( store,nodeid,modelid,prop,value ):
    if (nodeid in store.shadows)==False: return # unknown shadow
    shadow = store.shadows[nodeid]
    if (modelid in shadow)==False: return # unknow shadowmodel
    shadowmodel = shadow[modelid]

    shadowmodel['props'][prop] = value #update the value #TODO Check that the reference structure is correct

    store.emit('updateshadowmodel',prop,value,shadowmodel) # shadow emits a key, value ,model


## shadow add wire listener, updates shadow state from orign model state
# producer string uri of the producer property
# consumer string uri of the consumer property
def shadowaddwirelistener( store,producer,consumer ):

    nodeid,modelid,prop = tuple(producer.split('/'))

    if (nodeid in store.shadows)==False: return # no such shadow

    shadow = store.shadows[nodeid]

    if (modelid in shadow)==False: return # no such shadowmodel
      
    shadowmodel = shadow[modelid] 

    if (prop in shadowmodel['props'])==False: return # no such property

    if (prop in shadowmodel['wires'])==False: # create a wire disctioniary if needed
      shadowmodel['wires'][prop] = {}

    if (prop in shadowmodel['wires'])==True:    
      shadowmodel['wires'][prop][consumer] = '' # create a wire to the consumer

    store.emit('shadowaddwire',producer,consumer)

## shadow remove wire listener, updates shadow state from orign model state
# producer string uri of the producer property
# consumer string uri of the consumer property
def shadowremovewirelistener( store,producer,consumer ):

    nodeid,modelid,prop = tuple(producer.split('/'))

    if (nodeid in store.shadows)==False: return # no such shadow

    shadow = store.shadows[nodeid]

    if (modelid in shadow)==False: return # no such shadowmodel
      
    shadowmodel = shadow[modelid] 

    if (prop in shadowmodel['wires'])==False: return # no such proprty
    
    del shadowmodel['wires'][prop][consumer]  # remove wire to the consumer

    store.emit('shadowremovewire',producer,consumer)

## shadow add model, updates shadow state from orign model state
# model dictionary of the model state
def shadowaddmodel( store,model ):

    nodeid = model['nodeid']
    modelid = model['id']

    if (nodeid in store.shadows)==False: return # no such shadow

    shadow = store.shadows[nodeid]  

    shadow[modelid] = model #assign the shadowmodel

    store.emit('shadowaddmodel',shadow,model)


## shadow remove model, updates shadow state from orign model state
# nodeid string
# modelid string
def shadowremovemodel( store,nodeid,modelid ):
    
    if (nodeid in store.shadows)==False: return # no such shadow
      
    shadow = store.shadows[nodeid]  

    if (modelid in shadow)==False: return # no such shadowmodel

    del  store.shadows[nodeid][modelid]  # delete the shadow model
    
    store.emit('shadowremovemodel',nodeid,modelid)
