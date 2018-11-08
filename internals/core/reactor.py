import mutations
from config import nodekey
from queue import send

##react to an incoming command
# @param command string
# @param data list
def react(command, data, store):

  #update model action
  if command=='udm':
    nodeid,modelid,prop,value = tuple(data)
    if nodekey == nodeid:
      return mutations.updatemodel(store, nodeid, modelid, prop, value)
    send('udm', data, nodeid)
  
  #wire action
  if command=='w':
    producer,_ = tuple(data)
    nodeid,_,_ = tuple(producer.split('/'))
    return send('awl', data,nodeid)

  #unwire action
  if command=='uw':
    producer,_ = tuple(data)
    nodeid,_,_ = tuple(producer.split('/'))
    return send('rwl', data, nodeid)

  #add wiew wire listener action
  if command=='awl':
    producer, consumer = tuple(data)
    return mutations.addwirelistener(store, producer, consumer) 

  #remove wiew wire listener action
  if command=='rwl':
    producer,consumer = tuple(data)
    return mutations.removewirelistener(store, producer, consumer)

  #add shadow listener action
  if command=='asl':
    shadownodid, = tuple(data)
    return mutations.addshadowlistener(store, shadownodid)

  #remove shadow listener action
  if command=='rsl':
    shadownodid, = tuple(data)
    return mutations.removeshadowlistener(store, shadownodid)

  #add brick action
  if command=='ab':
    bricktype, = tuple(data)
    if nodekey == nodeid:
      return mutations.addbrick(store, bricktype)

  #remove brick action
  if command=='rb':
    modelid, = tuple(data)
    return mutations.removemodel(store, modelid)
 
  #discover action
  if command=='d':
    tonodeid, = tuple(data)
    model = store.models['1']
    return send('ad', [model.toDescription(), model.nodeid], tonodeid )
 

  """ from here on master node only """

  #add description action
  if command=='ad':
    description, nodeid = tuple(data)
    return mutations.adddescription(store, description, nodeid)

  #add shadow action
  if command=='ash':
    shadownodeid, shadow = tuple(data)
    return mutations.addshadow(store, shadownodeid,shadow)

  #remove shadow action
  if command=='rsh':
    shadownodeid, = tuple(data)
    return mutations.removeshadow(store, shadownodeid)

  #update shadow model action
  if command=='udsm':
    nodeid, modelid, prop, value = tuple(data)
    return mutations.updateshadowmodel(store, nodeid, modelid, prop, value)

  #shadow add wire listener action
  if command=='sawl':
    producer, consumer = tuple(data)
    return mutations.shadowaddwirelistener(store, producer, consumer)

  #shadow remove wire listener action
  if command=='srwl':
    producer, consumer = tuple(data)
    return mutations.shadowremovewirelistener(store, producer, consumer)

  #shadow add model action
  if command=='sam':
    model, = tuple(data)
    return mutations.shadowaddmodel(store, model)

  #shadow remove model action
  if command=='srm':
    nodeid, modelid = tuple(data)
    return mutations.shadowremovemodel(store, nodeid, modelid)

  #shadow add action
  if command=='shadow':
    nodeid, = tuple(data)
    return send('asl',[nodekey],nodeid)

  #shadow remove action
  if command=='unshadow':
    nodeid, = tuple(data)
    return send('rsl',[nodekey],nodeid)

    

"""  
  #route request action
  if command=='rq':
    source,target,hops = tuple(data)
    return routerequest ( source,target,hops,fro )

  #route response action
  if command=='rr':
    source,target,hops = tuple(data)
    return routeresponse ( source,target,hops,fro )
"""