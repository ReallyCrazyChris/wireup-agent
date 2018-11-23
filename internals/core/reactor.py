import mutations
from config import nodekey

sendqueue = []
receivequeue = []

def send(*data):
    if  nodekey == data[0]: # data[0] is the to nodeid 
        receivequeue.append(data)
    else:
        sendqueue.append(data)

def receive(data):
    receivequeue.append(data)

def react():
    """ processed the receivequeue"""
    for data in receivequeue:
        if  nodekey == data[1]:  # data[1] is the tonodeid   
          locals()[data[2]](*data) # data[2] is the command
    receivequeue.clear()
    # TODO garbatge collector      

def udm(fro, to, command, modelid, prop, value, salt=None):
    if to == nodekey: # forward to intended nodeid
        mutations.updatemodel(modelid, prop, value, salt=None)
        return
    send(to, command, modelid, prop, value, salt)

def w(fro, to, command, producer, consumer):
    """ request this agent to create a wire with another agent """
    send(producer[0],'awl', producer,consumer)

def uw(fro, to, command, producer, consumer):
    """ request this agent to create a wire with another agent """
    send(producer[0],'rwl', producer,consumer)

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

def announce(fro='all'):
    """ announces the produc description to all or a specific node"""
    mutations.announce(fro)
 
def ad(fro, to, command, discovered):
    """ adddiscovered """
    mutations.adddiscovered(discovered)
