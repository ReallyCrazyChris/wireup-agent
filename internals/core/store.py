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
    if ('*' in self.ev) == True:    
      for callback in self.ev['*']:
        callback(*args)
  

  def serialize(self):
      pass