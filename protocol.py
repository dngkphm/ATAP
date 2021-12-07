'''
tracks the states of the protocols

Not error proof
'''


'''
3 stages follow in succession
leader sends request "REQ" -> precommit
send back to leader "ACK"
leader sends to prepare -> prepare
send back to leader "PRE"
leader sends to commit -> commit
send back to leader "COM"

No pending 3PC -> "NAK"

if invalid or timeout or leader sends "NAK" -> "NAK"
'''
class T3PC():
    request = None
    precom = None
    commit = None
    leader = None
    def __init__(self,leader=False):
        self.request = None
        self.precom = None
        self.commit = None
        self.leader = leader
    def clear(self):
        self.request = None
        self.precom = None
        self.commit = None
    def __repr__(self):
        return "3PC: "+self.getNext()
    def next(self,msg):
        if self.commit != None:
            return
        if self.commit == None and msg == "COM" and self.precom != None:
            self.commit = msg
        if self.precom == None and msg == "PRE" and self.request != None:
            self.precom = msg
        if self.request == None and msg == "REQ" and self.commit == None:
            self.request = msg
        if msg == "NAK":
            self.clear()
            return
    def getNext(self):
        if self.request == None:
            return "REQ"
        if self.precom == None:
            return "PRE"
        if self.commit == None:
            return "COM"
        if self.request != None and self.precom != None and self.commit != None:
            return "ACK"
        return "NAK"

    
