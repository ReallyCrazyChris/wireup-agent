from config import nodekey
from bencode import bencode, bdecode

queue = {} # table of destinations
actions = []

#send groups messages together by desitnation
# @param command string
# @param args list
# @param tonodeid string identifier of the recipient node
def send(command, args, tonodeid):
    if  nodekey == tonodeid:
        receive(bdecode(bencode([command,args])))
    else:
        if (tonodeid in queue) == False:
            queue[tonodeid] =  [nodekey,tonodeid]  #create a queue for the destinaiton, push form and to

        if (tonodeid in queue) == True:
            queue[tonodeid].insert(0,[command,args]) #push on the  args
  
def receive(action):
    actions.append(action)

def process(react):
    for i in range(len(actions)):
        action = actions.pop(0)
        react(action[0],action[1])
