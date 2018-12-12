from model import Model
from driver import startdriver, stopdriver

class Product(Model):

  def __init__(self):
      super(Product, self).__init__()
    
      self.clazz='Product'
      self.type = 'ilike'
      self.version = '0.0.1'

      self.meta = {
        'imageurl'    :{'index':0, 'type':'url',    'display':'image',  'group':'info', 'label':'Image'},  
        'company'     :{'index':1, 'type':'string', 'display':'text',   'group':'info', 'label':'Company'},
        'name'        :{'index':2, 'type':'string', 'display':'text',   'group':'info', 'label':'Name'},
        'description' :{'index':3, 'type':'string', 'display':'text',   'group':'info', 'label':'Description'}, 
        'push':{'index':4, 'type':'boolean', 'display':'state', 'group':'control', 'label':'Push' },
        'sayilike':{'index':5, 'type':'boolean', 'display':'button', 'group':'control', 'label':'Say I Like' },
      }

      self.props = {
        'imageurl':'https://www.cameolight.com/out/media/image/cameo_header_lighteffects.jpg',
        'company':'CRUSIUS',
        'name':'I Like',
        'description':'a IoT enabled button',
        'push': False,
        'sayilike': False,
      }

  def start(self):
      print('starting product CRUSIUS I Like')
      startdriver(self)

      # push change event handler
      self.on('push',lambda product, prop, value : print('push event',product.id, prop, value))
      # sayilike change event handler
      self.on('sayilike',lambda product, prop, value : print('sayilike event',product.id, prop, value))

  def stop(self):
      print('stopping product CRUSIUS I Like')
      stopdriver(self)
      
      self.commit('push', False)
      self.commit('sayilike', False)

  def pushHandler(self, product, prop, value):
      print('property {} set to new value {}'.format(prop, value))
      # self.commit('push', False)
  def sayilikeHandler(self, product, prop, value):
      print('property {} set to new value {}'.format(prop, value))
      # self.commit('sayilike', False)
      
  def toDescription(self):
      return [self.clazz,self.type,self.props['imageurl'],self.props['company'],self.props['name'],self.props['description']]
