from model import Model

class Brick(Model):

  def __init__(self):
    super(Brick, self).__init__()
    
    self.clazz = 'Brick'
    self.type = 'logic_or'
    self.meta = {
      'imageurl'    :{'index':0, 'type':'url',    'display':'image',  'group':'info', 'label':'Image'},  
      'name'        :{'index':1, 'type':'string', 'display':'text',   'group':'info', 'label':'Name'},
      'description' :{'index':2, 'type':'string', 'display':'text',   'group':'info', 'label':'Description'}, 
      'inputA'      :{'index':3, 'type':'boolean', 'display':'toggle', 'group':'control', 'label':'inputA' },
      'inputB'      :{'index':4, 'type':'boolean', 'display':'toggle', 'group':'control', 'label':'inputB' },
      'output'      :{'index':5, 'type':'boolean', 'display':'state', 'group':'control', 'label':'output' },
    }

    self.props = {
      'imageurl':'https://www.cameolight.com/out/media/image/cameo_header_lighteffects.jpg',
      'name':'Logic OR',
      'description':'if inputA OR inputB then output ',
      'inputA': False,
      'inputB': False,
      'output': False
    }

  def start(self,store):
    self.on('inputA',self.evaluate)
    self.on('inputB',self.evaluate)

  def stop(self,store):
    print('stopping product WireUP WireUP Thing')
    self.commit('output', False)

  def evaluate(self, store, prop, value):
    if self.props['inputA'] or self.props['inputB']:
        self.commit('output', True)
    else:
        self.commit('output', False)

  def toDescription(self):
    return [self.clazz,self.type,self.props['imageurl'],self.props['name'],self.props['description']]
