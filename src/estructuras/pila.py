from estructuras.listaEnlazada import LinkedList

"""
Implementación optimizada de pila (LIFO) usando lista enlazada propia
Cumple con requisitos de implementación desde cero y nomenclatura descriptiva
"""

class Stack:
    def __init__(self):
        """
        Inicializa una pila vacía usando lista enlazada propia.
        """
        self.stackData = LinkedList()
    
    def addElementToStack(self, elementData):
        """
        Agrega un elemento en el tope de la pila.
        
        Args:
            elementData: Dato a apilar
        """
        # Crear nuevo nodo y actualizar referencias
        newNode = LinkedList.Node(elementData)
        newNode.next = self.stackData.head
        self.stackData.head = newNode
        self.stackData.length += 1
    
    def removeElementFromStack(self):
        """
        Remueve y devuelve el elemento del tope de la pila.
        
        Returns:
            Elemento removido
            
        Raises:
            IndexError: Si la pila está vacía
        """
        if self.isStackEmpty():
            raise IndexError("Operación inválida: pila vacía")
        
        elementData = self.stackData.head.data
        self.stackData.head = self.stackData.head.next
        self.stackData.length -= 1
        
        return elementData
    
    def getTopElementFromStack(self):
        """
        Obtiene el elemento en el tope de la pila sin removerlo.
        
        Returns:
            Elemento en el tope o None si está vacía
        """
        return self.stackData.head.data if not self.isStackEmpty() else None
    
    def isStackEmpty(self):
        """
        Verifica si la pila contiene elementos.
        
        Returns:
            True si está vacía, False de lo contrario
        """
        return self.stackData.length == 0
    
    def getStackSize(self):
        """
        Devuelve el número de elementos en la pila.
        
        Returns:
            Cantidad de elementos
        """
        return self.stackData.length
    
    def clearStack(self):
        """Vacía completamente la pila"""
        self.stackData.head = None
        self.stackData.length = 0
    
    def __str__(self):
        """
        Representación en cadena de la pila (solo para depuración).
        
        Returns:
            Cadena descriptiva del estado de la pila
        """
        elements = LinkedList()
        currentNode = self.stackData.head
        
        while currentNode:
            elements.append(str(currentNode.data))
            currentNode = currentNode.next
        
        return "Stack: [" + " <- ".join(elements) if elements.length > 0 else "Pila Vacía"
