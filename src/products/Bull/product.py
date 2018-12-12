from model import Model
from driver import startdriver, stopdriver

class Product(Model):

  def __init__(self):
      super(Product, self).__init__()
    
      self.clazz='Product'
      self.type = 'bull'
      self.version = '0.0.1'

      self.meta = {
        'imageurl'    :{'index':0, 'type':'url',    'display':'image',  'group':'info', 'label':'Image'},  
        'company'     :{'index':1, 'type':'string', 'display':'text',   'group':'info', 'label':'Company'},
        'name'        :{'index':2, 'type':'string', 'display':'text',   'group':'info', 'label':'Name'},
        'description' :{'index':3, 'type':'string', 'display':'text',   'group':'info', 'label':'Description'}, 
        'push':{'index':4, 'type':'boolean', 'display':'state', 'group':'control', 'label':'Push' },
        'saybull':{'index':5, 'type':'boolean', 'display':'button', 'group':'control', 'label':'Say Bull' },
        'led':{'index':6, 'type':'boolean', 'display':'toggle', 'group':'control', 'label':'LED' },
      }

      self.props = {
        'imageurl':'https://www.cameolight.com/out/media/image/cameo_header_lighteffects.jpg',
        'company':'Buttonz',
        'name':'Bull',
        'description':'an IoT device enabled by WireUP',
        'push': False,
        'saybull': False,
        'led': False,
      }

  def start(self):
      print('starting product Buttonz Bull')
      startdriver(self)

      # push change event handler
      # self.on('push',lambda product, prop, value : print('push event',product.id, prop, value))
      # saybull change event handler
      # self.on('saybull',lambda product, prop, value : print('saybull event',product.id, prop, value))
      # led change event handler
      # self.on('led',lambda product, prop, value : print('led event',product.id, prop, value))

  def stop(self):
      print('stopping product Buttonz Bull')
      stopdriver(self)
      
      self.commit('push', False)
      self.commit('saybull', False)
      self.commit('led', False)

  def pushHandler(self, product, prop, value):
      print('property {} set to new value {}'.format(prop, value))
      # self.commit('push', False)
  def saybullHandler(self, product, prop, value):
      print('property {} set to new value {}'.format(prop, value))
      # self.commit('saybull', False)
  def ledHandler(self, product, prop, value):
      print('property {} set to new value {}'.format(prop, value))
      # self.commit('led', False)
      
  def toDescription(self):
      return [self.clazz,self.type,self.props['imageurl'],self.props['company'],self.props['name'],self.props['description']]
