import sys
import socket
import structures
import manager
import log
import connector
import packet
import database
import CONFIG
import node
import protocol

def _defping():
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = ("127.0.0.1",3080)
    sckt.bind(addr)
    msg= b"!"
    try:
        sckt.listen(10)
        print("waiting")
        clientsocket,address = sckt.accept()
        print("get",address)
        clientsocket.send(msg)
        #msg = sckt.recv(1024)
        #print(msg)
    except socket.error as e:
        print("socket error")
        sckt = None
        print(e)
    sckt.close()

def main():
    addr_n1 = ("127.0.0.1",8001)
    n1 = node.Node(0,addr_n1)
    addr_n2 = ("127.0.0.1",8000)
    n1.addNode(1,addr_n2[0],addr_n2[1])
    messages = ["REQ","PRE","COM"]
    compackets = [packet.createPacket(str(n1.nodeID)+":"+str(n1.getNextTID()),"CMT",msg) for msg in messages]
    print(compackets)
    n1.fetchMessage(addr_n1)
    print(n1.tMgr.TXNs)

    msg = n1.getMessage()
    print(n1.tMgr.TXNs)
    processMessage(msg)
    
'''
def example():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 1234))
    s.listen(5)

    while True:
        # now our endpoint knows about the OTHER endpoint.
        clientsocket, address = s.accept()
        print(f"Connection from {address} has been established.")
if __name__ == "__main__":
    _defping()
'''
