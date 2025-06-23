from estructuras.listaEnlazada import LinkedList

class Queue:
    def __init__(self):
        self.queueData = LinkedList()
        self.lastNode = None
    
    def addElementToQueue(self, elementData):
        newNode = LinkedList.Node(elementData)
        if self.queueData.isEmpty():
            self.queueData.head = newNode
            self.lastNode = newNode
        else:
            self.lastNode.next = newNode
            self.lastNode = newNode
        self.queueData.length += 1
    
    def removeElementFromQueue(self):
        if self.isQueueEmpty():
            raise IndexError("Operacion invalida: cola vacia")
        
        elementData = self.queueData.head.data
        self.queueData.head = self.queueData.head.next
        self.queueData.length -= 1
        
        if self.isQueueEmpty():
            self.lastNode = None
            
        return elementData
    
    def isQueueEmpty(self):
        return self.queueData.length == 0
    
    def getFirstElementInQueue(self):
        return self.queueData.head.data if not self.isQueueEmpty() else None
    
    def getQueueSize(self):
        return self.queueData.length
    
    def clearQueue(self):
        self.queueData.head = None
        self.lastNode = None
        self.queueData.length = 0