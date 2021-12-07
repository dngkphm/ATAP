'''
Handles network connections and operations
'''
import socket
import CONFIG
import packet

socket.setdefaulttimeout(CONFIG.PING_MAX_LIMIT)

'''
A class that manages all connections between nodes


@Variables
connections:
Remembers all connections to each address
It is a dictionary with the NodeID as the key, (IP,port) as its values

nCtrl:
the network controller that redirects the connections to the fastest/most live

nLead:
the socket of the node leader of the cluster
'''
class NetworkController:
    connections = {}
    nCtrl = None #the network controller
    nLead = None #the leader node
    num_connections = 0
    

    '''
    creates a socket binded to an IP and port number
    socket is live/connected
    '''
    def connect(self,ip,port,sockettype=socket.AF_INET,streamtype=socket.SOCK_STREAM):
        scket = socket.socket(sockettype,streamtype)
        addr = (ip,port)
        scket.bind(addr)
        try:
            scket.connect(addr)
            print("connected: ",str(ip),str(port))
        except socket.error as e:
            print("socket error")
        self.connection = scket
        return

    def sendAll(msg):
        return
    



'''
checks for a valid connection
'''
def checkConnection(ip=CONFIG.CONNECT_IP_DEFAULT,port=CONFIG.CONNECT_PORT_DEFAULT):
    scket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    addr = (ip,port)
    conn = False
    try:
        scket.connect(addr)
        conn = True
    except socket.error as e:
        print("Could not connect to ",str(ip),str(port),sep=":")
        print(e)
    scket.close()
    return conn

'''
closes a valid connection
'''
def closeSocket(ip,port):
    scket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    addr = (ip,port)
    scket.bind(addr)
    scket.close()

'''
Encodes data into bytes and sends thru connection
'''
def sendData(ip,port,data,limit=CONFIG.PACK_MAX_LIMIT):
    byte_data = data.encode(CONFIG.CONNECT_ENCODE_DEFAULT)
    scket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    addr = (ip,port)
    scket.bind(addr)
    scket.listen(CONFIG.PING_MAX_LIMIT)
    try:
        recvsocket,recvaddr = scket.accept()
        recvsocket.send(byte_data)
        print("data sent")
    except socket.error as e:
        print("error sending data")
        print(e)
    scket.close()

'''
Waits to receive data from this connection
'''
def recvData(ip,port,limit:int=CONFIG.PACK_MAX_LIMIT):
    sckt = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    addr = (ip,port)
    msg = None
    try:
        sckt.connect(addr)
        print("connected")
        msg = sckt.recv(limit)
    except socket.error as e:
        print(e)
    sckt.close()
    if msg == None:
        return
    return msg.decode(CONFIG.CONNECT_ENCODE_DEFAULT)


'''
A clean way to create connections between nodes
It's a class in case I forget to close the connection
'''
#DEFUNCT bc binded sockets cannot be reused
class Connection:
    bind = None
    port = CONFIG.CONNECT_PORT_DEFAULT
    ip = CONFIG.CONNECT_IP_DEFAULT
    def __init__(self,ip,port,sockettype=socket.AF_INET,streamtype=socket.SOCK_STREAM):
        scket = socket.socket(sockettype,streamtype)
        addr = (ip,port)
        scket.bind(addr)
        self.bind = scket
        self.port = port
        self.ip = ip
    def close(self):
        self.bind.close()
    def connect(self):
        self.bind.connect((self.ip,self.port))
    def __del__(self):
        self.bind.close()
    

    
    
