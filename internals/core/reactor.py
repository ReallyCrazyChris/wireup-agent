import mutations
from config import nodekey
from asyncio import sleep
from bencode import bencode, bdecode

reactqueue = []
sendgroup = {} # table of destinations

def send(command, args, tonodeid):
    if  nodekey == tonodeid: 
        print('internal communicatio  ...',[command,args])
        reactQueueAppend(bdecode(bencode([command,args]))) # TODO is there a better way, faster ?
    else:
        if (tonodeid in sendgroup) == False:
            sendgroup[tonodeid] =  [nodekey,tonodeid]  #create a sendgroup for the destinaiton, push form and to

        if (tonodeid in sendgroup) == True:
            sendgroup[tonodeid].insert(0,[command,args]) #push on the  args

# adds data to the reactqueue
def reactQueueAppend(data):
    reactqueue.append(data)

def react():
    for i in range(len(reactqueue)): # TODO better way ?
        action = reactqueue.pop(0)
        processCommand(action[0],action[1]) # TODO use *data ?   

##react to an incoming command
# @param command string
# @param data list
def processCommand(command, data):

  print('react',command,data)

  #update model action
  if  command=='udm':
      nodeid = data[0]
      if nodekey == nodeid:
        return mutations.updatemodel(*data)
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
    return mutations.addwirelistener(producer, consumer) 

  #remove wiew wire listener action
  if command=='rwl':
    producer,consumer = tuple(data)
    return mutations.removewirelistener(producer, consumer)

  #add shadow listener action
  if command=='asl':
    shadownodid, = tuple(data)
    return mutations.addshadowlistener(shadownodid)

  #remove shadow listener action
  if command=='rsl':
    shadownodid, = tuple(data)
    return mutations.removeshadowlistener(shadownodid)

  #add brick action
  if command=='ab':
    bricktype, = tuple(data)
    # TODO where is nodeid 
    if nodekey == nodeid:
      return mutations.addbrick(bricktype)

  #remove brick action
  if command=='rb':
    modelid, = tuple(data)
    return mutations.removemodel(modelid)
 

  # TODO store needed here :(
  #discover action
  if command=='d':
    #tonodeid, = tuple(data)
    #model = store.models['1']
    #return send('ad', [model.toDescription(), model.nodeid], tonodeid )
    pass
 

  """ from here on master node only """

  #add description action
  if command=='ad':
    description, nodeid = tuple(data)
    return mutations.adddescription(description, nodeid)

  #add shadow action
  if command=='ash':
    shadownodeid, shadow = tuple(data)
    return mutations.addshadow(shadownodeid,shadow)

  #remove shadow action
  if command=='rsh':
    shadownodeid, = tuple(data)
    return mutations.removeshadow(shadownodeid)

  #update shadow model action
  if command=='udsm':
    nodeid, modelid, prop, value = tuple(data)
    return mutations.updateshadowmodel(nodeid, modelid, prop, value)

  #shadow add wire listener action
  if command=='sawl':
    producer, consumer = tuple(data)
    return mutations.shadowaddwirelistener(producer, consumer)

  #shadow remove wire listener action
  if command=='srwl':
    producer, consumer = tuple(data)
    return mutations.shadowremovewirelistener(producer, consumer)

  #shadow add model action
  if command=='sam':
    model, = tuple(data)
    return mutations.shadowaddmodel(model)

  #shadow remove model action
  if command=='srm':
    nodeid, modelid = tuple(data)
    return mutations.shadowremovemodel(nodeid, modelid)

  #shadow add action
  if command=='shadow':
    nodeid, = tuple(data)
    return send('asl',[nodekey],nodeid)

  #shadow remove action
  if command=='unshadow':
    nodeid, = tuple(data)
    return send('rsl',[nodekey],nodeid)