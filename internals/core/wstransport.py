from config import ip
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from reactor import receive
from bencode import bencode, bdecode
from store import Store 

store = Store()

def updateAllClients(websocketserver,store):
    for fileno in websocketserver.connections:
        connection = websocketserver.connections[fileno]
        msg = bencode(['update',store.toDict()])
        connection.sendMessage(msg)

class WssHandler(WebSocket):

    def handleMessage(self):
        
        action = bdecode( self.data )
        print(action)
        receive(action)
            
    def handleConnected(self):
        #print(self.address, 'connected')
        msg = bencode(['update',store.toDict()])
        self.sendMessage(msg)

    def handleClose(self):
        pass
        #print(self.address, 'closed')

def getwebsocket():
    websocketserver = SimpleWebSocketServer(ip, 9090, WssHandler)   
    # register for all store events
    store.on('*', lambda *args: updateAllClients(websocketserver,store))  

    return websocketserver
