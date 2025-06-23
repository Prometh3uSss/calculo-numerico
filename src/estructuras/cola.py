from estructuras.listaEnlazada import LinkedList

class Queue:
    def __init__(self):
        """
        Implementación de cola FIFO usando lista enlazada propia.
        Cumple con requisitos de implementación desde cero.
        """
        self.queueData = LinkedList()
        self.lastNode = None
    
    def addElementToQueue(self, elementData):
        """
        Agrega un elemento al final de la cola.
        
        Args:
            elementData: Dato a encolar
        """
        newNode = LinkedList.Node(elementData)
        if self.queueData.isEmpty():
            self.queueData.head = newNode
            self.lastNode = newNode
        else:
            self.lastNode.next = newNode
            self.lastNode = newNode
        self.queueData.length += 1
    
    def removeElementFromQueue(self):
        """
        Remueve y devuelve el elemento del frente de la cola.
        
        Returns:
            Elemento removido
            
        Raises:
            IndexError: Si la cola está vacía
        """
        if self.isQueueEmpty():
            raise IndexError("Operación inválida: cola vacía")
        
        elementData = self.queueData.head.data
        self.queueData.head = self.queueData.head.next
        self.queueData.length -= 1
        
        if self.isQueueEmpty():
            self.lastNode = None
            
        return elementData
    
    def isQueueEmpty(self):
        """
        Verifica si la cola contiene elementos.
        
        Returns:
            True si está vacía, False de lo contrario
        """
        return self.queueData.length == 0
    
    def getFirstElementInQueue(self):
        """
        Obtiene el elemento al frente de la cola sin removerlo.
        
        Returns:
            Elemento en el frente o None si está vacía
        """
        return self.queueData.head.data if not self.isQueueEmpty() else None
    
    def getQueueSize(self):
        """
        Devuelve el número de elementos en la cola.
        
        Returns:
            Cantidad de elementos
        """
        return self.queueData.length
    
    def clearQueue(self):
        """Vacía completamente la cola"""
        self.queueData.head = None
        self.lastNode = None
        self.queueData.length = 0