'''
Handles messages and packaging of data

Data deliverable. Contains queries or ACKs between
Types:
1) Request  (REQ)
2) Query    (QRY)
3) ACKS/Commit  (CMT-ACK/NAK)
4) Network Info (NET-SYN/FIN)
5) Error Handling   (ERR)
6) Other    (NON)
'''
import CONFIG

'''
Data that will be sent over the network. Contains formatted data and size
'''
'''
class Message:
    data = str()
    size = int()
    def __init__(self,msg:str):
        self.data = msg #MUST format message first!!
        self.size = len(msg)
'''

'''returns the length of the message'''
def lenMSG(msg:str)->int:
    in1 = msg.find(CONFIG.MSG_DELIM_OPEN)
    return int(msg[:in1])
  
'''
Breaks the message into readable chunks and appends the size
@params: message in string format, (max message size)
@result: a list of readable strings
'''
def formatMSG(msg:str,size_limit:int=CONFIG.MSG_MAX_LIMIT)->[str]:
    #delim_sz = len(CONFIG.MSG_DELIM_OPEN+CONFIG.MSG_DELIM_CLOSE)
    num_chunks = CONFIG.upFlDiv(len(msg),size_limit)
    messages = list()
    #break message into chunks
    for i in range(num_chunks):
        tmp_msg = ""
        len_msg = 0
        if num_chunks > 1:
            len_msg = size_limit
        else:
            len_msg = len(msg)
        tmp_msg = str(len_msg)+CONFIG.MSG_DELIM_OPEN+\
                  msg[(i*len_msg):((i+1)*len_msg)]+CONFIG.MSG_DELIM_CLOSE
        messages.append(tmp_msg)
    return messages

'''
Deciphers message into a string format (strips message)
Returns None if the message is not readable
'''
def readMSG(msg:str)->str:
    in1 = msg.find(CONFIG.MSG_DELIM_OPEN)
    in2 = msg.find(CONFIG.MSG_DELIM_CLOSE)
    if in1<0 or in2<0:
        return None
    return msg[in1+len(CONFIG.MSG_DELIM_OPEN):in2]

def checkMSG(msg:str)->bool:
    marker = msg.find(CONFIG.MSG_DELIM_OPEN)
    size = int(msg[:marker])
    t_msg = msg[marker+len(CONFIG.MSG_DELIM_OPEN):-len(CONFIG.MSG_DELIM_OPEN)]
    if size != len(t_msg):
        print("Invalid message")
        return False
    return True
        

'''
Packet
The node will read the message and package it as a packet for further processing

<Header,Pre-proccessing,Data>
Header: PacketID <NodeID| TransactionID| Network{Dst,Src,time,key}>
PP: Type, Length
Data: payload
'''
'''
class Packet():
    header = str()
    pre = str()
    data = str()
    size = 0
    
    def __init__(self,ID:str,form:str,data:str):
        self.ID = ID
        self.pre = form
        self.data = data
        return
'''


def lenPKT(msg:str)->int:
    ini = msg.find(CONFIG.PACK_DELIM_OPEN)
    if ini == -1:
        return -1
    length = int(msg[:ini])
    return length

def readPKT(packet:str)->str:
    ini = packet.find(CONFIG.PACK_DELIM_OPEN)
    inf = packet.find(CONFIG.PACK_DELIM_CLOSE)
    size = int(packet[:ini])
    
    t_data = packet[(ini+len(CONFIG.PACK_DELIM_OPEN)):inf]

    if not checkPKT(packet):
        print("invalid packet")
        return None,None,None

    in1 = t_data.find(CONFIG.PACK_DELIM_SEP)
    packID = t_data[:in1]
    in2 = t_data[in1+len(CONFIG.PACK_DELIM_SEP):].find(CONFIG.PACK_DELIM_SEP) + in1+len(CONFIG.PACK_DELIM_SEP)
    form = t_data[in1+len(CONFIG.PACK_DELIM_SEP):in2]
    message = t_data[in2+len(CONFIG.PACK_DELIM_SEP):]
    return packID,form,message


def packPKT(packID,form,msg:str)->str:
    '''
    "size//<packID//type//payload//>"
    '''
    header = str(packID)
    pre = str(form)
    t_data = header+CONFIG.PACK_DELIM_SEP+pre+CONFIG.PACK_DELIM_SEP+msg
    length = len(t_data)+len(CONFIG.PACK_DELIM_OPEN+CONFIG.PACK_DELIM_CLOSE)
    return str(length) + CONFIG.PACK_DELIM_OPEN + t_data + CONFIG.PACK_DELIM_CLOSE

def checkPKT(packet)->bool:
    ini = packet.find(CONFIG.PACK_DELIM_OPEN)
    inf = packet.find(CONFIG.PACK_DELIM_CLOSE)
    size = int(packet[:ini])-len(CONFIG.PACK_DELIM_OPEN+CONFIG.PACK_DELIM_CLOSE)
    
    t_data = packet[(ini+len(CONFIG.PACK_DELIM_OPEN)):inf]

    if len(t_data) != size:
        print("invalid packet")
        return False
    return True

'''For small packets only
'''
def createPacket(tid,form,msg):
    message = formatMSG(msg)[0]
    packet = packPKT(tid,form,message)
    return packet

def main():
    messages = formatMSG("*args, **kwargs) Perform a string formatting\
operation. The string on which this method is called can contain literal\
text or replacement fields delimited by braces {}. Each replacement field\
contains either the numeric index of a positional argument, or the name of\
a keyword argument. Returns a copy of the string where each replacement\
field is replaced with the string value of the corresponding argument.")
    msgs = list()
    for m in messages:msgs.append(Message(m))
    print(msgs)
