from config import nodekey
from typecoersion import coerce

txqueue = {}

class Store():

  def __init__(self):
    self.ev = {}
    self.nodeid = nodekey
    self.models = {}
    self.shadowlisteners = {}
    self.discovered = {}
    self.shadows = {}

  #EVENT
  #on - adds an event callback
  # @param n string event name
  # @param c fuction event callback
  def on(self,name,callback):
    if ((name in self.ev) == False): self.ev[name] = []  #create a queue for the destinaiton, push form and to
    if ((name in self.ev) == True):  self.ev[name].append(callback)   #push on the command and data

  #emit - emits an named event with arguments
  # @param n String event name
  # @param ... Arguments passed to the event callback
  def emit(self,name,*args):
    if (name in self.ev) == True:
      for callback in self.ev[name]:
        callback(*args)


  #addmodel - adds a Model instance to the store
  # @param self refence to store
  # @param model subclass object of Model
  def addmodel(self,model):

    if (model.id in self.models) == True: return # model exists
      
    if model.id == False: # provide an id if the model has none
      id = 1
      while (str(id) in self.models) == True:
        id  += 1

    model.id = str(id)          #model.id is a string
    model.nodeid = self.nodeid  # provide the model with a nodeid
    
    self.models[model.id] = model

    model.start(self) # lifecycle start

    for shadowlistenerid in self.shadowlisteners: # propagate to shadow listeners
      queuetx('sam',[model.toDict()],shadowlistenerid)

  def removemodel(self,modelid):
  
    if (modelid in self.models) == False: return # model does'nt exists  
    model = self.models[modelid]
    model.stop(self)

    for shadowlistenerid in self.shadowlisteners: # propagate to shadow listeners
      queuetx('srm',[model.nodeid,model.id],shadowlistenerid)

    model = None
    # TODO garbage collection
 
  ## updatemodel update model
  # @param modelid integer
  # @param prop string
  # @param value any
  # @param s store reference
  def updatemodel( self,nodeid,modelid,prop,value ):

    if (modelid in self.models)==False: return # unknowm model

    model = self.models[modelid]

    proptype = model.meta[prop]['type']

    coercedvalue = coerce(value,proptype) # coerces the value to the property type

    if model.props[prop] == coercedvalue: return # no value change

    model.props[prop] = coercedvalue # assigns the new value

    model.emit(prop, self, prop, model.props[prop]) # emit a property value change event

    # propagate to shadow models
    for shadownodeid in self.shadowlisteners:
      queuetx('udsm',[nodeid,modelid,prop,coercedvalue],shadownodeid)
          
    if (prop in model.wires)==False: return # any wire listeners for prop      
    
    wirelisteners = model.wires[prop]
    # propagate the value to the wire listeners
    for listeneruri in wirelisteners:
      listenernodeid,listnermodlid,listenerprop = tuple(listeneruri.split('/'))
      queuetx('udm',[listenernodeid,listnermodlid,listenerprop,coercedvalue],listenernodeid)

  ## add wire listener, to be nitified when a model property changes
  # producer string uri of the producer property
  # consumer string uri of the consumer property
  def addwirelistener( self,producer,consumer):

    pnodeid,pmodelid,pprop = tuple(producer.split('/'))
    cnodeid,cmodelid,cprop = tuple(consumer.split('/'))

    if (pmodelid in self.models)==False: return # no such model

    model = self.models[pmodelid]  

    if (pprop in model.props)==False: return # no such key  

    if (pprop in model.wires)==False: # cretae a dict for the prop if there is none
      model.wires[pprop] = {}

    if (pprop in model.wires)==True:
      model.wires[pprop][consumer] = ''

    for shadowlistenerid in self.shadowlisteners: # propagate to shadow listeners
      queuetx('sawl',[producer,consumer],shadowlistenerid)  

    queuetx('udm',[cnodeid,cmodelid,cprop,model.props[pprop]],cnodeid)   # propagate the value to the property listener

    # save the store state to non-volatile memory, so the wire state is remembered
    self.serialize()

  ## remove wire listener
  # producer string uri of the producer property
  # consumer string uri of the consumer property
  def removewirelistener( self,producer,consumer ):

    pnodeid,pmodelid,pprop = tuple(producer.split('/'))
    # cnodeid,cmodelid,cprop = tuple(consumer.split('/'))

    if (pmodelid in self.models)==False: return # no such model

    model = self.models[pmodelid]  

    if (pprop in model.props)==False: return # no such key  

    if (pprop in model.wires)==False: return # no such wire

    if (pprop in model.wires)==True:
      if (consumer in model.wires[pprop])==True:
        del model.wires[pprop][consumer]

    for shadowlistenerid in self.shadowlisteners: # propagate to shadow listeners
      queuetx('srwl',[producer,consumer],shadowlistenerid)  

    # save the store state to non-volatile memory, so the wire state is remembered
    self.serialize()

  ## add shadow listener, to be notified when a model updates 
  # listenerdata table shadoe lisener nodeid
  # shadowlisteners table
  # models table
  def addshadowlistener( self,listenernodeid ):

    self.shadowlisteners[listenernodeid] = True # register the shadow listener
    
    models = {}

    for modelid in self.models:
      models[modelid] = (self.models[modelid]).toDict()
    
    queuetx('ash',[self.nodeid,models],listenernodeid) # notify the listener the current models


  ## removeshadowlistener
  # listenerdata table shadoe lisener nodeid
  # shadowlisteners table
  # models table
  def removeshadowlistener( self,listenernodeid ):
    if listenernodeid in self.shadowlisteners:
      del self.shadowlisteners[listenernodeid] # unregister the shadow listener
      queuetx('rsh',[self.nodeid],listenernodeid) # notify the listener the current models

  ## toDic converts the Store to a dictionary
  def toDict(self):
    
    models = {}

    for modelid in self.models:
      models[modelid] = self.models[modelid].toDict()

    return {
      'nodeid':self.nodeid,
      'models':models,
      'shadowlisteners':self.shadowlisteners,
      'discovered':self.discovered,
      'shadows':self.shadows,
      'bricks': bricks() # dictionary of installed bricks
    }

    
  # save the store state to non-volatile memory, so the state is remembered
  def serialize( self ):
    pass



##queuetx groups messages together by desitnation for transmission
# @param command string
# @param data list
# @param tonodeid string identifier of the recipient node
def queuetx(command,data,tonodeid):

  #if (tonodeid == nodekey):  #  its me. dont queue just react
  #  return react( command,data,to,nodekey,store )

  if ((tonodeid in txqueue) == False):
    txqueue[tonodeid] =  [nodekey,tonodeid]  #create a queue for the destinaiton, push form and to
 
  if ((tonodeid in txqueue) == True):
    txqueue[tonodeid].insert(0,data)   #push on the command and data
    txqueue[tonodeid].insert(0,command)   #push on the command and data

##react to an incoming command
# @param command string

# @param data list
# @param to string node identifier of the recipient (this node) 
# @param fro string node identifier of the sender (another node) 
def react( command,data,to,fro,store ):

  #update model action
  if command=='udm':
    nodeid,modelid,prop,value = tuple(data)
    if store.nodeid == nodeid: # is this for me
      return store.updatemodel( nodeid,modelid,prop,value )
    # nope ist for something else  
    return queuetx('udm',[nodeid,modelid,prop,value],nodeid)

  #wire action
  if command=='w':
    producer,_ = tuple(data)
    nodeid,_,_ = tuple(producer.split('/'))
    return queuetx( 'awl',data,nodeid )

  #unwire action
  if command=='uw':
    producer,_ = tuple(data)
    nodeid,_,_ = tuple(producer.split('/'))
    return queuetx( 'rwl',data,nodeid )

  #add wiew wire listener action
  if command=='awl':
    producer,consumer = tuple( data )
    return store.addwirelistener( producer,consumer ) 

  #remove wiew wire listener action
  if command=='rwl':
    producer,consumer = tuple( data )
    return store.removewirelistener( producer,consumer )

  #add shadow listener action
  if command=='asl':
    shadownodid, = tuple( data )
    return store.addshadowlistener( shadownodid )

  #remove shadow listener action
  if command=='rsl':
    shadownodid, = tuple( data )
    return store.removeshadowlistener( shadownodid )

  #add brick action
  if command=='ab':
    brickname, = tuple( data )
    brickinstance = importlib.import_module('bricks.'+str( brickname ) ).Brick()
    store.addmodel( brickinstance )

  #remove brick action
  if command=='rb':
    modelid, = tuple( data )
    return store.removemodel( modelid )

  #discover action
  if command=='d':
    tonodeid, = tuple( data )
    return announce( store.models['1'], tonodeid)

# announce the product on the network
## @param tonodeid string oprional - nodeid of a specific other WireUP afent
## s table - reference to the store
def announce(model,tonodeid='all'):
  return queuetx('ad', [model.toDescription(), model.nodeid], tonodeid )

##  discovery of all WireUP nodes onthe network segement
def discover():
  queuetx('d',[nodekey],'all') 

## shadow another node
# nodeid string nodeid of the other node
# s table reference to the store
def shadow ( nodeid ):
  queuetx('asl',[nodekey],nodeid)

## unshadow another node
# nodeid string nodeid of the other node
# s table reference to the store
def unshadow ( nodeid ):
  queuetx('rsl',[nodekey],nodeid)

## add a brick to a remote node
# nodeid string nodeid that should add the brick
# s table referenc to the store
def addbrick( nodeid,brickname ):
  queuetx('ab',[brickname],nodeid)

## remove a brick to a remote node
# uri string nodeid/modelid of the brick to remove
# s table referenc to the store
def removebrick( brickuri ):
  nodeid,modelid = tuple(brickuri.split('/'))
  queuetx('rb',[nodeid,modelid],nodeid)

## request a remote agent to create a wire
# @param pu producerUri the property uri of the eventstream source
# @param cu consumerUri the property uri of the eventstream sink
def wire( producer,consumer ):
  nodeid,_,_ = tuple(consumer.split('/'))
  queuetx('w',[producer,consumer],nodeid)

## request a remote agent to remove a wire
# @param pu producerUri the property uri of the eventstream source
# @param cu consumerUri the property uri of the eventstream sink
def unwire( producer,consumer  ):
  nodeid,_,_ = tuple(consumer.split('/'))
  queuetx('uw',[producer,consumer],nodeid)

  ## set a property value of a remote or local model
# @param to uri of a remote model
# @param prop string name of a property
# @param value any property value to set
def update( to,prop,value ):
  nodeid,modelid = tuple(to.split('/'))
  queuetx('udm',[nodeid,modelid,prop,value],nodeid)