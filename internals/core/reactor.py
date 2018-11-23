import mutations
from config import nodekey

sendqueue = []
receivequeue = []

def send(*data):
    if  nodekey == data[1]: # data[1] is the to nodeid 
        receivequeue.append(data)
    else:
        sendqueue.append(data)

def receive(data):
    receivequeue.append(data)

def react():
    """ processed the receivequeue"""
    for packet in receivequeue:
       
        if  not packet[1] in [nodekey, 0]: return # not for me and not a multicast
        if  not packet[2] in actions: return # not a known action 

        print('calling action',actions[packet[2]])

        actions[packet[2]](*packet)            

    receivequeue.clear()
    # TODO garbatge collector ??      

def udm(fro, to, command, modelid, prop, value, salt=None):
    if to == nodekey: # forward to intended nodeid
        mutations.updatemodel(modelid, prop, value, salt=None)
        return
    send(nodekey, to, command, modelid, prop, value, salt)

def w(fro, to, command, producer, consumer):
    """ request this agent to create a wire with another agent """
    send(nodekey, producer[0],'awl', producer,consumer)

def uw(fro, to, command, producer, consumer):
    """ request this agent to create a wire with another agent """
    send(nodekey, producer[0],'rwl', producer,consumer)

def awl(fro, to, command, producer, consumer):
    """ adds a wire listener """
    mutations.addwirelistener(producer, consumer)     

def rwl(fro, to, command, producer, consumer):
    """ removes a wire listener """
    mutations.removewirelistener(producer, consumer)   

def asl(fro, to, command, nodeid):
    """ add twin listener """
    mutations.addshadowlistener(nodeid)

def rsl(fro, to, command, nodeid):
    """ remove twin listener """
    mutations.removeshadowlistener(nodeid)

def ab(fro, to, command, packagename):
    """ add brick """
    mutations.addbrick(packagename)

def rb(fro, to, command, modelid):
    """ remove brick / model """
    mutations.removemodel(modelid)

def d(fro, to, command):
    """ discover responds with an anncoucnement to the requester """
    mutations.announce(fro)
 
def ad(fro, to, command, description):
    """ adds a description of a discovered product or service """
    print('react ad',fro, to, command, description)
    mutations.adddescription(fro,description)

def announce(fro='all'):
    """ announces the produc description to all or a specific node"""
    mutations.announce(fro)

actions = {
    'udm':udm,
    'w':w,
    'uw':uw,
    'awl':awl,
    'rwl':rwl,
    'asl':asl,
    'rsl':rsl,
    'ab':ab,
    'rb':rb,
    'd':d,
    'ad':ad
}    