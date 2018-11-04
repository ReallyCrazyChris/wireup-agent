from store import Store
from product import Product
from mutations import addmodel
from actions import announce
from transport import listen

store = Store()
product = Product()
addmodel(store, product)

#store.on('adddescription',lambda description,fro: print('adddescription', description))
#store.on('adddescription',lambda description,fro: wireup.shadow(nodekey))
#store.on('addshadow',lambda shadow,shadows: print('shadow event'))
#store.on('removeshadow',lambda shadow,shadows: print('unshadow event'))
#store.on('addshadow',lambda shadow,shadows: wireup.update(nodekey+'/'+'1','name','updated_name'))
#product.on('name',lambda value,updatedmodel: print(value,updatedmodel.props))
#product.on('name',lambda value,updatedmodel: wireup.wire(nodekey+'/'+'1/name',nodekey+'/'+'1/company'))
#store.on('updateshadowmodel',lambda prop,value,shadowmodel: print(shadowmodel))

# announce a descritpion of the dial model on the network using multicast
announce(product,'all')
#discover()
listen(store) 