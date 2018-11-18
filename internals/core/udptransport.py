import socket

from config import ip, port, multiaddr
from bencode import bencode, bdecode
from reactor import reactQueueAppend, sendgroup

rt = {} # routing table

def getsocket():
    # bind to a network adapter on ip and port
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # Create a IPv4/UDP socket  
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Reuse the network adapter for other protocols
    sock.bind((ip,port))     # Bind to a network adapter on port

    # register as a multicast listener with the router.
    mreq=socket.inet_aton(multiaddr)+socket.inet_aton(ip) # calcualte the multicast receiver enrt
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)    # Register as a muticast receiver 
    sock.setblocking(False)

    return sock

def receiveudp (sock):
    try:
        msg, address = sock.recvfrom(4096) # Buffer size is 2048. Change as needed.
    except: 
        # exceptions will be continoulsy thrown due to the non-blocking of recivefrom
        pass
    else:
        if msg:
            print(msg)
            packets = bdecode(msg)
            if packets == False: return 
            #print(packets)
            to = packets.pop()   #  pop off to nodeid value
            fro = packets.pop()  #  pop off from nodeid value

            if fro:
                rt[fro] = (address[0],address[1])  # update the routing table

            while len(packets): # TODO better bad packedt detection, use itterator
                data = packets.pop()
                reactQueueAppend(data)

def sendudp (sock):
    for nodeid in sendgroup:

        packets = sendgroup[nodeid]
    
        if packets:
            data = bencode(packets)
            if nodeid == "all" : #  multicast
                sock.sendto(data, (multiaddr,port))
            
            elif (nodeid in rt)==True : #  unicast 
                sock.sendto(data, rt[nodeid])
            
            else:
                print('destination unknown for', nodeid) 

    sendgroup.clear()