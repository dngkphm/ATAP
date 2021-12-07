'''
Handles multi-threaded transactions for nodes

PoolManager Class:
Sorts incoming TxN's/Queries for queueing or release purposes
Manages TxN's across threads into a pool

TxnManager Class:
handles incoming transactions into an ordered queue

QManager Class:
handles outgoing transactions and tags requests

ThreadManager:
synchronously assigns TxNs to each node
'''

import threading
import structures


class ThreadManager(threading.Thread):
    processes = list()
    def __init__(self):
        self.processes.append(0) #parent process
        return

    def lock(self,res,pid:int=0):
        return
    def release(self,lock):
        return
    def start(self):
        return
    
class PoolManager(ThreadManager):
    TXNs = None

    def __init__(self):
        self.TXNs = structures.SmartQ()
        return
    
    '''
    returns the next transaction in the thread's buffer
    '''
    def getNext(self,pid:int=0):
        #j = self.lock(TXNs,pid)
        item = self.TXNs.pop().value[0]
        #release(j)
        return item
    
    '''
    Add the next transaction to the buffer
    @params: (transaction, priority level), process id
    @result: nothing
    '''
    def pushNext(self,item,priority=2,pid:int=0):
        #j = self.lock(pid,TXNs)
        self.TXNs.add(item,priority)
        #release(j)

    def getAll(self)->list:
        items = [] #ordered by priority
        while not self.TXNs.isEmpty():
            items.append(self.TXNs.pop().value[0])
        return items

    def sendAll(self,items:list):
        for item in items:
            self.TXNs.add(item.priority)



'''For testing purposes ONLY'''
def main():
    qManager = PoolManager()
    return
