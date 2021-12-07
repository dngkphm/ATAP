import socket
import sys
import structures
import manager
import log
import connector
import packet
import database
import CONFIG
import node
import protocol
import dns.resolver
from dns import reversename

def lookup(server,spec='A'):
    result = dns.resolver.query(server,spec)
    thing = list()
    for item in result:
        thing.append(item)
    return thing

def storeLocally(records):
    return



def _defping():
    greetmsg = b'hello world!'
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = ("127.0.0.1",3080)
    #sckt.bind(addr)
    try:
        sckt.connect(addr)
        print("connected")
        #sckt.send(greetmsg)
        msg = sckt.recv(1024)
        print(msg)
    except socket.error as e:
        print("socket error")
    if sckt != None:
        sckt.close()
    return msg.decode('utf-8')

'''testing purposes'''
def main():
    addr_n1 = ("127.0.0.1",8000)
    n1 = node.Node(1,addr_n1)
    addr_n2 = ("127.0.0.1",8001)
    n1.addNode(0,addr_n2[0],addr_n2[1])
    messages = ["REQ","PRE","COM"]
    compackets = [packet.createPacket(str(n1.nodeID)+":"+str(n1.getNextTID()),"CMT",msg) for msg in messages]
    print(compackets)
    for msg in compackets:
        n1.queueMessage(msg)
    print(n1.qMgr.TXNs)
    n1.pushMessage(addr_n2)
    
    

'''
def main():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 1234))

    msg = s.recv(1024)
    print(msg.decode("utf-8"))
if __name__ == "__main__":
    _defping()
        
    '''
