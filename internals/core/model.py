class Model():

  #Constructor
  def __init__(self):
    self.clazz='Model'  
    self.type = 'model'
    self.id = False
    self.nodeid = False
    self.eventlisteners = {}
    self.wires = {}
    self.meta = {}
    self.props = {}
    self.ev = {}

  #Event
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

  def start(self,store):
    pass
    
  def stop(self,store):
    pass

  def toDescription(self):
    raise NotImplementedError #you want to override this on the child classes

  def toDict(self):
    return {
      'clazz': self.clazz,
      'type' : self.type, 
      'id' : self.id, 
      'nodeid' : self.nodeid, 
      #'eventlisteners' : self.eventlisteners,
      'wires' : self.wires,
      'meta' : self.meta,
      'props' : self.props
    }  
