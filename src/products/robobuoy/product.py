from model import Model
from driver import startdriver, stopdriver

class Product(Model):

  def __init__(self):
      super(Product, self).__init__()
    
      self.clazz='Product'
      self.type = 'robobuoy'
      self.version = '0.0.1'

      self.meta = {
        'imageurl'    :{'index':0, 'type':'url',    'display':'image',  'group':'info', 'label':'Image'},  
        'company'     :{'index':1, 'type':'string', 'display':'text',   'group':'info', 'label':'Company'},
        'name'        :{'index':2, 'type':'string', 'display':'text',   'group':'info', 'label':'Name'},
        'description' :{'index':3, 'type':'string', 'display':'text',   'group':'info', 'label':'Description'}, 
        'active':{'index':4, 'type':'boolean', 'display':'toggle', 'group':'control', 'label':'active' },
        'steer':{'index':5, 'type':'integer', 'display':'number', 'group':'control', 'label':'steer' },
        'surge':{'index':6, 'type':'integer', 'display':'number', 'group':'control', 'label':'thrust', 'units':'m' },
        'minpwm':{'index':7, 'type':'integer', 'display':'number', 'group':'settings', 'label':'min pwm' },
        'gain':{'index':8, 'type':'integer', 'display':'number', 'group':'settings', 'label':'steer gain' },
        'maxpwm':{'index':9, 'type':'integer', 'display':'number', 'group':'settings', 'label':'max pwm' },
      }

      self.props = {
        'imageurl':'https://www.cameolight.com/out/media/image/cameo_header_lighteffects.jpg',
        'company':'RoboRegatta',
        'name':'Robobuoy',
        'description':'Autonamous Robotic Buoy',
        'active': False,
        'steer': 0,
        'surge': 0,
        'minpwm': 40,
        'gain': 1,
        'maxpwm': 115,
      }

  def start(self):
      print('starting product RoboRegatta Robobuoy')
      startdriver(self)

      # active change event handler
      # self.on('active',lambda product, prop, value : print('active event',product.id, prop, value))
      # steer change event handler
      # self.on('steer',lambda product, prop, value : print('steer event',product.id, prop, value))
      # surge change event handler
      # self.on('surge',lambda product, prop, value : print('surge event',product.id, prop, value))
      # minpwm change event handler
      # self.on('minpwm',lambda product, prop, value : print('minpwm event',product.id, prop, value))
      # gain change event handler
      # self.on('gain',lambda product, prop, value : print('gain event',product.id, prop, value))
      # maxpwm change event handler
      # self.on('maxpwm',lambda product, prop, value : print('maxpwm event',product.id, prop, value))

  def stop(self):
      print('stopping product RoboRegatta Robobuoy')
      stopdriver(self)
      
      self.commit('active', False)
      self.commit('steer', 0)
      self.commit('surge', 0)
      self.commit('minpwm', 40)
      self.commit('gain', 1)
      self.commit('maxpwm', 115)

  def activeHandler(self, product, prop, value):
      print('property {} set to new value {}'.format(prop, value))
      # self.commit('active', False)
  def steerHandler(self, product, prop, value):
      print('property {} set to new value {}'.format(prop, value))
      # self.commit('steer', 0)
  def surgeHandler(self, product, prop, value):
      print('property {} set to new value {}'.format(prop, value))
      # self.commit('surge', 0)
  def minpwmHandler(self, product, prop, value):
      print('property {} set to new value {}'.format(prop, value))
      # self.commit('minpwm', 40)
  def gainHandler(self, product, prop, value):
      print('property {} set to new value {}'.format(prop, value))
      # self.commit('gain', 1)
  def maxpwmHandler(self, product, prop, value):
      print('property {} set to new value {}'.format(prop, value))
      # self.commit('maxpwm', 115)
      
  def toDescription(self):
      return [self.clazz,self.type,self.props['imageurl'],self.props['company'],self.props['name'],self.props['description']]
