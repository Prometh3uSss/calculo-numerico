from estructuras.listaEnlazada import LinkedList

class Stack:
    def __init__(self):
        self.stackData = LinkedList()
    
    def addElementToStack(self, elementData):
        # Crear nuevo nodo y actualizar referencias
        newNode = LinkedList.Node(elementData)
        newNode.next = self.stackData.headNode
        self.stackData.headNode = newNode
        self.stackData.listLength += 1
    
    def removeElementFromStack(self):
        if self.isStackEmpty():
            raise IndexError("Operacion invalida: pila vacia")
        
        elementData = self.stackData.headNode.data
        self.stackData.headNode = self.stackData.headNode.next
        self.stackData.listLength -= 1
        
        return elementData
    
    def getTopElementFromStack(self):
        return self.stackData.headNode.data if not self.isStackEmpty() else None
    
    def isStackEmpty(self):
        return self.stackData.listLength == 0
    
    def getStackSize(self):
        return self.stackData.listLength
    
    def clearStack(self):
        self.stackData.headNode = None
        self.stackData.listLength = 0
    
    def __str__(self):
        elements = LinkedList()
        currentNode = self.stackData.headNode
        
        while currentNode:
            elements.append(str(currentNode.data))
            currentNode = currentNode.next
        
        return "Stack: [" + " <- ".join(elements) if elements.length > 0 else "Pila Vacia"
