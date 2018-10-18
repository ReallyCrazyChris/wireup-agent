from model import Model

class Product(Model):

  def __init__(self):
    super(Product, self).__init__()
    
    self.type = 'Product'

    self.meta = {
      'imageurl'    :{'index':0, 'type':'url',    'display':'image',  'group':'info', 'label':'Image'},  
      'company'     :{'index':1, 'type':'string', 'display':'text',   'group':'info', 'label':'Company'},
      'name'        :{'index':2, 'type':'string', 'display':'text',   'group':'info', 'label':'Name'},
      'description' :{'index':3, 'type':'string', 'display':'text',   'group':'info', 'label':'Description'}, 
      'volume'      :{'index':4, 'type':'integer','display':'number', 'group':'control', 'label':'Volume'},   
      'power'       :{'index':5, 'type':'boolean','display':'state',  'group':'control', 'label':'Power'},
      'reset'       :{'index':6, 'type':'boolean','display':'button', 'group':'control', 'label':'Reset'},
      'onoff'       :{'index':7, 'type':'boolean','display':'toggle', 'group':'control', 'label':'On / Off'},
      'size'        :{'index':8, 'type':'integer','display':'select', 'group':'settings', 'label':'Size',   'options':['small', 'medium', 'large']}, 
      'route'       :{'index':9, 'type':'integer','display':'choice', 'group':'settings', 'label':'Route',  'options':['scenic', 'shortest', 'fastest']}         
    }

    self.props = {
      'imageurl':'https://www.cameolight.com/out/media/image/cameo_header_lighteffects.jpg',
      'company':'WireUP',
      'name':'Thing',
      'description':'IOT enabled thing',
      'volume':100,
      'power':False,
      'reset':False,
      'onoff':False,
      'size':1,
      'route':1
    }
    
  def toDescription(self):
    return [self.type,self.props['imageurl'],self.props['company'],self.props['name'],self.props['description']]
