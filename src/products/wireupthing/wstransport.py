from config import ip
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from actor import doaction
from bencode import bencode, bdecode
from store import Store
from plugins.bricks import bricks 

store = Store()

def storeData():
    return {
        'discovered':store.discovered, 
        'shadows':store.shadows,
        'bricks':bricks()
    }

def updateAllClients(websocketserver,store):
    for fileno in websocketserver.connections:
        connection = websocketserver.connections[fileno]
        msg = bencode(['update',storeData()])
        # print(len(msg))
        connection.sendMessage(msg)

class WssHandler(WebSocket):

    def handleMessage(self):
        action = bdecode( self.data )
        print(self.data)
        doaction(action)
            
    def handleConnected(self):
        print(self.address, 'connected')
        msg = bencode(['update',storeData()])
        self.sendMessage(msg)

    def handleClose(self):
        print(self.address, 'closed')

def getwebsocket():
    websocketserver = SimpleWebSocketServer(ip, 9090, WssHandler)   
    # register for all store events
    store.on('*', lambda *args: updateAllClients(websocketserver,store))  

    return websocketserver
