from config import nodekey

queue = {} # message queue

##send groups messages together by desitnation for transmission
# @param command string
# @param args list
# @param tonodeid string identifier of the recipient node
def send(command, args, tonodeid):

    if (tonodeid in queue) == False:
        queue[tonodeid] =  [nodekey,tonodeid]  #create a queue for the destinaiton, push form and to

    if (tonodeid in queue) == True:
        queue[tonodeid].insert(0,args) #push on the  args
        queue[tonodeid].insert(0,command) #push on the command