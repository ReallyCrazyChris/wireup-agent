from product import Product
from mutations import addmodel, announce
from runner import listen

product = Product()
addmodel(product)
# announce a descritpion of the dial model on the network using multicast
announce(product, 'all')
# discover()
listen()
