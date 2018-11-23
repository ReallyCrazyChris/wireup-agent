from config import nodekey
#from bricks.install import bricks

class Store():

  _instance = None #singleton
  def __new__(class_, *args, **kwargs):
      if not isinstance(class_._instance, class_):
          class_._instance = object.__new__(class_, *args, **kwargs)
      return class_._instance

  def __init__(self):
    self.pointer = 0
    self.ev = {}
    self.nodeid = nodekey
    self.models = {}
    self.shadowlisteners = {}
    self.discovered = {}
    self.twins = {}


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
    if ('*' in self.ev) == True:    
      for callback in self.ev['*']:
        callback(*args)
    

  def model(self, modelid):
      """ retrives a model by modelid """  
      return self.models[modelid]

  def addmodel(self, model):

      model.start() # lifecycle start

  def removemodel(self, modelud):
      """ removes a model from the store """
      pass

  def injectmodleid(self, model):
      """ gives a model its id """
      if model.id == False: # provide an id if the model has none
          self.pointer +=1
          model.id = str(self.pointer)   #model.id is a string
          model.nodeid = nodekey     # provide the model with a nodeid

  def twin(self, nodeid):
      """ retrives a twin by id """

  def addtwin(self, twin):
      """adds a model to the store"""
      pass

  def removetwin(self, nodeid):
      """ removes a model from the store """
      pass



