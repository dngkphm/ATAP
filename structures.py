'''
Contains data structures used in the project

1) Queue
2) SmartQ (Priority Queue w/twist)
3) Buffer
'''

class Node:
    value = None
    nextNode = None
    def __init__(self,val=None,node=None):
        self.value = val
        self.node = node
    def __repr__(self):
        return "Node("+str(self.value)+")->"


class Queue:
    top = None
    end = None
    length = 0
    def __init__(self,node:Node=None):
        self.top = node
        self.end = node
        if node != None:
            self.length += 1
    def __del__(self):
        self.clear()
    def pop(self):
        if(self.top == None):
            return None
        item = self.top
        self.top = self.top.nextNode
        self.length -= 1
        if (self.top == None):
            self.end = None
        return item
    def add(self,val):
        if type(val) != None:
            item = Node(val,None)
        else:
            item = val
        if (self.top == None):
            self.top = item
        if (self.end == None):
            self.end = item
            self.length += 1
            return
        self.end.nextNode = item
        self.end = item
        self.length += 1
        
        #for handling chained nodes
        prevNode = self.end
        curNode = self.end.nextNode
        while(curNode != None):
            self.length += 1
            prevNode = currNode
            curNode = curNode.nextNode
        self.end = prevNode
        
    def peek(self):
        return self.top
    def peekEnd(self):
        return self.end
    def isEmpty(self):
        return self.top==None
    def clear(self):
        temp = self.top
        while (temp != None):
            del temp.value
            temp = temp.nextNode
        self.top = None
        self.end = None
        length = 0
    def __repr__(self):
        values = []
        n = self.top
        while(n != None):
            l = str(n.value)
            print(l)
            values.append(l)
            n = n.nextNode
        a = "Queue: "+str(values)
        return a
    

'''[Node(object, priority level),...]'''
class SmartQ(Queue):
    lowestP = 0 #the lowest priority level (default items = 2)
    #adjusting the lowestP acts as a bypass
    
    def __init__(self,level:int=0):
        if level < 0:
            level = 0
        self.lowestP = level
        return

    def pop(self,level:int=-1):
        if level < 0:
            level = self.lowestP
        if(self.top == None):
            return None

        curNode = self.top
        item = curNode
        prevNode = self.top
        while (curNode != None):
            if (curNode.value[1] <= level):
                #if first item in the list
                #else just change pointers
                if prevNode == curNode:
                    item = self.top
                    self.top = self.top.nextNode
                else:
                    item = curNode
                    prevNode.nextNode = curNode.nextNode
                item.nextNode = None
                self.length -= 1
                break
            else:
                level += 1
                continue
            prevNode = curNode
            curNode = curNode.nextNode
        return item
        
    def add(self,val,level:int=2):
        if level < 0:
            level = self.lowestP
        #handle Node and bare val as inputs
        if type(val) != Node:
            item = Node((val,level),None)
        else:
            item = Node((val.value,level),None)
        #handle empty case
        if (self.top == None):
            self.top = item
        if (self.end == None):
            self.end = item
            self.length += 1
            return
        
        prevNode = self.top
        curNode = self.top
        #first item in the list
        if curNode.value[1] > level:
            self.top = item
            item.nextNode = curNode
            self.length += 1
            return
        #iterate the rest of the list
        while (curNode != None and level >= curNode.value[1]):
            prevNode = curNode
            curNode = curNode.nextNode
        #insertion
        item.nextNode = curNode 
        prevNode.nextNode = item
        self.length += 1
        #reached the end of the list
        if (curNode == None):
            self.end = item
        return

    def setLowestP(self,level:int):
        if level <= 0:
            self.lowestP = 0
            return
        self.lowestP = level
        return
        
    
class Buffer:
#private
    _queue = None
    _queue_sz = 100
    _queue_max = 1000
    _queue_cur = 0

#public
    def __init__(self,maxsize:int=1000):
        self._queue = list()
        self._queue_max = maxsize
        self._queue_cur = 0
        return
    
    def __del__(self):
        for item in self._queue:
            del item
            self._queue_cur -= 1
        del self._queue
        self._queue_cur = 0
        self._queue_sz = 0
        return
        
    
    def push(self,element):
        self._queue.append(element)
        self._queue_cur += 1
        if self._queue_sz < self._queue_cur:
            self._queue_sz += 1
        return
    
    def pop(self):
        
        return
    def peek(self):
        return

    def getSize(self):
        return self._queue_sz
    def getMaxCapacity(self):
        return self._queue_max
    def getIndex(self):
        return self._queue_cur

'''For testing purposes ONLY'''
def main():
    s = SmartQ()
    import random
    priority = []
    for i in range(10):
        priority.append(random.randint(0,10))
    print(priority,s.lowestP)
    for i in range(10):
        s.add(i,priority[i])
        #print("S",s)
    print("Level: ",s.lowestP)
    print(s)
    print(s.pop().value)
