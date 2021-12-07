'''
Node Class:

Acts as the template for server nodes
Nodes receive, process, and send messages between nodes
Nodes log and commit transactions
Nodes also synchronize other nodes in the network by relaying network information
(ARP, Forwarding tables) under supervision of a network controller

Processing Protocol are as follows:
Sending:
1) Node packages the request in a message
2) Node sends the message to the query pool
3) Query Pool manager selects and sends message to the other nodes
4) Node awaits confirmation

Receiving:
1) Received requests from other nodes enter a TxN pool
2) TxN pool manager pulls the request and unpackages the message
3) Node confirms it has received the package
4) Node begins to process the package

Processing:
1) Upon confirmation, the node begins to order messages
2) Messages are processed. If it is a database TxN, the node processes it in loggin
3) Node determines the next steps

The following is configurable:
1) Leader node
2) Multi-threading enabled
3) Memory limit (queue size)
4) Protocol
'''

import structures
import manager
import log
import connector
import packet
import database
import CONFIG
import threading
import datetime
import protocol

class Node:
    #log
    logfile = None
    logdir = CONFIG.LOG_DIR
    #database
    db = None
    #managers
    qMgr = None #QManager loads transactions for sending
    tMgr = None #TManager buffers incoming data for processing
    #network
    nodes = None
    nCtrl = None #the network controller
    nLead = None #the leader node
    num_connections = 0
    ip_addr = None #(ip,port)
    #transactions
    _t_id = 0 #increment for every transaction sent
    nodeID = 0 #assigned by the network controller
    #Threads for querying and transactions (Default = 1)
    qThd = None
    tThd = None
    
#public
    def __init__(self,ID:int,nodeIP:str):
        self.qMgr = manager.PoolManager()
        self.nodeID = ID
        self.tMgr = manager.PoolManager()
        self.ip_addr = nodeIP
        self.nodes = dict()
        self.protocol = protocol.T3PC()
        self.tempTXN = ""
        self.logfile = log.LogFile()
        return
    def __del__(self):
        del self.qMgr
        del self.tMgr
        del self.nodes
        return
    def __repr__(self):
        return "Node "+self.nodeID

    #Node functions
    '''
    Unpack packet into message, read message to process accordingly
    '''
    def processMessage(self,pkt):
        p_id,form,message = packet.readPKT(pkt)
        if p_id == None:
            print("could not process the message")
            return
        result = self.evaluate(p_id,form,message)
        return result

    def getNextTID(self):
        t_id = self._t_id
        self._t_id += 1
        return t_id

    '''
    Pack message for sending
    Types:
        1) Request  (REQ)
        2) Query    (QRY)
        3) ACKS/Commit  (CMT-ACK/NAK)
        4) Network Info (NET-SYN/FIN)
        5) Error Handling   (ERR)
        6) Other    (NON)
    '''
    def packMessage(self,msg,form,t_id:int=0):
        if t_id <= self._t_id:
            t_id = getNextTID()
        p = packet.packPKT(str(self.nodeID)+":"+str(t_id),form,msg)
        return p

    '''Push next message into Txn pool
    '''
    def queueMessage(self,msg):
        #transform message into a packet
        self.qMgr.pushNext(msg)
        return
    
    '''Get next message from Q pool
    '''
    def getMessage(self):
        txn = self.tMgr.getNext()
        return txn

    #TRANSPORT
    '''Pull next message from other node's Q Pool into T pool
        Use THIS node's IP,Port for fetch
    '''
    def fetchMessage(self,connection):
        #txn = self.tMgr.fetchNext()
        #other qMgr.push()
        #this self.tMgr.getNext(qMgr)
        incomingMSG = connector.recvData(connection[0],connection[1])
        self.tMgr.pushNext(incomingMSG)
        
    '''Send data from the Q Pool to the other node's T Pool
        Use OTHER node's IP,Port for push
    '''
    def pushMessage(self,connection):
        #txn = self.qMgr.getMessage()
        #other = other tMgr.push()
        #this self.qMgr.pop()
        outgoingMSG = self.qMgr.getNext()
        connector.sendData(connection[0],connection[1],outgoingMSG)
    
    
    '''Move the following connection to the network controller'''

    '''Add the connection to the list of connected nodes
    @output: returns if successful/not
    '''
    def addNode(self,nodeID,ip,port):
        ''' IGNORE TO STOP HANGING CONNECTION
        if not connector.checkConnection(ip,port):
            return False
        '''
        addr = (ip,port)
        if nodeID not in self.nodes.keys():
            self.nodes[nodeID] = list()
        self.nodes[nodeID].append(addr)
        self.num_connections += 1
        return True

    def removeNode(self,nodeID):
        if not nodeId in self.nodes.keys():
            return
        connections = self.nodes[nodeID]
        for addr in connections:
            connector.closeSocket(addr[0],addr[1])
        del self.nodes[nodeId]
        self.num_connection -= 1
    
    '''End move'''
    ###PROTOCOL
    '''Filters messages accordingly and performs operations'''
    def evaluate(self,tid,form,msg):
        response = None
        if form == "REQ":
            #when receiving a request, wait for 3 phase protocol
            #drop the last 3PC and do this one
            if self.protocol.request != None:
                self.protocol.clear()
            self.tempTXN = msg
            self.protocol.next(form)
            return self.protocol.getNext()
        if form == "QRY":
            #update stats about the node (read file etc)
            #self.makeQuery(tid,msg)
            return
        if form == "CMT":
            #if commit != None, make query and commit
            self.protocol.next(packet.readMSG(msg))
            response = self.protocol.getNext()
            if response == "ACK":
                self.commitTXN(tid,self.tempTXN)
            return response
        if form == "NET":
            return
        if form == "ERR":
            self.report(tid,msg)
            return
        if form == "NON":
            return
        return response

    '''report failed commits or missing TXNs'''
    def report(self):
        return

    '''choose a leader node'''
    def elect(self):
        return
    
    '''Update DB'''
    def makeQuery(self,tid,message):
        if self.protocol.commit == None:
            return
        self.logfile.write_log(formatTXN(tid,message))
        print("written")
        
    '''View data from DB'''
    def viewQuery(self,tid):
        return
    
    '''Make updates to the network'''
    def parseNet(self,message):
        return

    '''Report errors to the system'''
    def report(self,message):
        return


    #LOGGING
    '''
    Send message into a packet, assign TxN id and other preprocessing data
    '''
    def orderTXN(self):
        #Threading not recommended, skip
        return
    '''
    Commit message into log
    '''
    def commitTXN(self,tid,message):
        if self.protocol.commit == None:
            return False
        self.logfile.write_log(formatTXN(tid,message))
        return True
    '''
    Revert log to # transaction
    '''
    def revert(self):
        return
    '''
    Commit log to the database, clear/create new log
    '''
    def updateDB(self):
        #txns = self.logfile.fetch_log(tid)
        #for t in txns:
        #    txn = t.strip('\n').split('\t')
        #    tID = txn[0]
        #    date = txn[1]
        #    script = txn[2]
        #    self.db.executeQuery(self.db._dbname,script,tID)
        #db.updateTable()
        #self.logfile._clear()
        return


'''get the time for the transaction'''
def formatTXN(tid,msg):
    time = str(datetime.datetime.now())
    head = tid
    data = msg
    result = head +"\t"+time+"\t"+data
    return result

'''
def createPacket(tid):
    message = packet.formatMSG("NAK")[0]
    packet = packet.packPKT(tid,"CMT",message)
    return packet
'''   

class LeaderNode (Node):
    def __init__(self):
        return

'''For testing purposes ONLY'''
def main():
    addr_n1 = ("127.0.0.1",8000)
    n1 = Node(1,addr_n1)
    addr_n2 = ("127.0.0.1",8080)
    n2 = Node(2,addr_n2)
    addr_n3 = ("127.0.0.1",8005)
    n3 = Node(3,addr_n3)

    '''adding nodes will be automated with network controller'''
    n1.addNode(n2.nodeID,addr_n2[0],addr_n2[1])
    n2.addNode(n1.nodeID,addr_n1[0],addr_n1[1])
    n1.addNode(n3.nodeID,addr_n3[0],addr_n3[1])
    n2.addNode(n3.nodeID,addr_n3[0],addr_n3[1])
    n3.addNode(n1.nodeID,addr_n1[0],addr_n1[1])
    
    print(n1.nodeID,n1.getNextTID())
    msg1 = packet.createPacket(str(n1.nodeID)+":"+str(n1.getNextTID()),"REQ","hello")
    n1.queueMessage(msg1)
    print(n1.qMgr.TXNs)

    #test protocol
    CMTmsg = ["REQ","PRE","COM"]
    compackets = [packet.createPacket(n1.nodeID,"CMT",msg) for msg in CMTmsg]
    print(compackets)
    for pkt in compackets:
        n1.tMgr.pushNext(pkt)
    print(n1.tMgr.TXNs.peek())
    for pkt in compackets:
        msg = n1.getMessage()
        print(msg)
        n1.processMessage(msg)


    #test connection t&q queues
    print(n1.nodes,n1.nodes[n2.nodeID][0])
    #start threading
    #n1.pushMessage(n1.nodes[n2.nodeID][0])
    #new thread
    #n2.fetchMessage(n2.nodes[n1.nodeID][0])
    
   
    print(n1.nodes,n1.num_connections)
    return
