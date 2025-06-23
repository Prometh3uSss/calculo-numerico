from estructuras.listaEnlazada import LinkedList

class Stack:
    def __init__(self):
        self.stackData = LinkedList()
    
    def addElementToStack(self, elementData):
        # Crear nuevo nodo y actualizar referencias
        newNode = LinkedList.Node(elementData)
        newNode.next = self.stackData.head
        self.stackData.head = newNode
        self.stackData.length += 1
    
    def removeElementFromStack(self):
        if self.isStackEmpty():
            raise IndexError("Operacion invalida: pila vacia")
        
        elementData = self.stackData.head.data
        self.stackData.head = self.stackData.head.next
        self.stackData.length -= 1
        
        return elementData
    
    def getTopElementFromStack(self):
        return self.stackData.head.data if not self.isStackEmpty() else None
    
    def isStackEmpty(self):
        return self.stackData.length == 0
    
    def getStackSize(self):
        return self.stackData.length
    
    def clearStack(self):
        self.stackData.head = None
        self.stackData.length = 0
    
    def __str__(self):
        elements = LinkedList()
        currentNode = self.stackData.head
        
        while currentNode:
            elements.append(str(currentNode.data))
            currentNode = currentNode.next
        
        return "Stack: [" + " <- ".join(elements) if elements.length > 0 else "Pila Vacia"
