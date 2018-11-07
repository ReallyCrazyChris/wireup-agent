from config import nodekey
from queue import send

# announce the product on the network
## @param tonodeid string oprional - nodeid of a specific other WireUP afent
## s table - reference to the store
def announce(model, tonodeid='all'):
    send('ad', [model.toDescription(), model.nodeid], tonodeid )

##  discovery of all WireUP nodes onthe network segement
def discover():
    send('d',[nodekey],'all') 

## shadow another node
# nodeid string nodeid of the other node
# s table reference to the store
def shadow (nodeid):
    print('sending shadow asl',nodeid)
    send('asl',[nodekey],nodeid)

## unshadow another node
# nodeid string nodeid of the other node
# s table reference to the store
def unshadow (nodeid):
    send('rsl',[nodekey],nodeid)

## add a brick to a remote node
# nodeid string nodeid that should add the brick
# s table referenc to the store
def addbrick(nodeid, brickname):
    send('ab',[brickname],nodeid)

## remove a brick to a remote node
# uri string nodeid/modelid of the brick to remove
# s table referenc to the store
def removebrick(brickuri):
    nodeid,modelid = tuple(brickuri.split('/'))
    send('rb',[nodeid,modelid],nodeid)

## request a remote agent to create a wire
# @param pu producerUri the property uri of the eventstream source
# @param cu consumerUri the property uri of the eventstream sink
def wire(producer, consumer):
    nodeid,_,_ = tuple(consumer.split('/'))
    send('w',[producer,consumer],nodeid)

## request a remote agent to remove a wire
# @param pu producerUri the property uri of the eventstream source
# @param cu consumerUri the property uri of the eventstream sink
def unwire(producer, consumer):
    nodeid,_,_ = tuple(consumer.split('/'))
    send('uw',[producer,consumer],nodeid)

## set a property value of a remote or local model
# @param to uri of a remote model
# @param prop string name of a property
# @param value any property value to set
def update(nodeid, modelid, prop, value):
    send('udm',[nodeid,modelid,prop,value],nodeid)

