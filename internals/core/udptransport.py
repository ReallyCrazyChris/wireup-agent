import socket
from bencode import bencode, bdecode
from reactor import receive, sendqueue, react

try: # try to make this work for both python37 and micropython
    import ustruct as struct            
except ImportError:
    import struct

rt = {} # routing table
port = 3300 # TODO find the port thans is least blocked by NAT's
multiaddr = '225.0.0.37'  # TOSO find a free but mostly acceptable address

def aton(ipv4address):
    """convert an IPv4 address to 32-bit packed binary format"""
    a = []
    for i in ipv4address.split('.'):
        a.append(int(str(i)))
    return struct.pack('BBBB', a[0],a[1],a[2],a[3])

def getsocket(ip):
    """creates a datagram socket and registers the ipaddress as a multicast listner"""   
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Reuse the network adapter for other protocols
    sock.bind((ip,port)) #bind to a network adapter on ip and port

    # register as a multicast listener with the router.
    mreq=aton(multiaddr) + aton(ip)
    print('mreq',multiaddr,ip,mreq)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)    # Register as a muticast receiver 
    #sock.setblocking(False)
    sock.settimeout(0.0001)
    return sock

def receiveudp (sock):
    """ receives datagram messages and queues them for processing, updates a routing table """
    try:
        data, address = sock.recvfrom(2048) # Buffer size is 2048. Change as needed.
    except Exception:
        pass
        # exceptions will be continoulsy thrown due to the non-blocking of recivefrom
    else:
        if data:
            # print('receiveudp', data, len(data))
      
            packet = bdecode(data)

            if packet == False: return 
    
            print('receive', packet)

            #to = packet.pop()   #  pop off to nodeid value
            #fro = packet.pop()  #  pop off from nodeid value
            fro = packet[0]
            if fro:
                rt[fro] = (address[0],address[1])  # update the routing table

            receive(packet)

def sendudp (sock):
    """ """
    for packet in sendqueue:

            nodeid = packet[1]
            data = bencode(packet)
            #print('sendudp',data)
            if nodeid == 0 : #  multicast
                print(sock.sendto(data, (multiaddr,port)) ,len(data))
            
            elif (nodeid in rt)==True : #  unicast 
                #print(sock.sendto(data, (multiaddr,port)) ,len(data))
                print(sock.sendto(data, rt[nodeid]), len(data))
            else:
                print('destination unknown for', nodeid)
                print('multicasting...') 
                print(sock.sendto(data, (multiaddr,port)) ,len(data))
    sendqueue.clear()
