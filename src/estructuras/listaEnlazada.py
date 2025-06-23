class Node:
    def __init__(self, elementData):
        """
        Inicializa un nodo para almacenar datos en estructuras enlazadas
        
        Args:
            elementData: Dato a almacenar en el nodo
        """
        self.elementData = elementData
        self.nextNode = None

class LinkedList:
    def __init__(self):
        """
        Implementación de lista enlazada simple con funcionalidad completa
        """
        self.headNode = None
        self.listLength = 0
    
    def addElementAtEnd(self, elementData):
        """
        Agrega un nuevo elemento al final de la lista
        
        Args:
            elementData: Dato a agregar
        """
        newNode = Node(elementData)
        
        if self.headNode is None:
            self.headNode = newNode
        else:
            currentNode = self.headNode
            while currentNode.nextNode:
                currentNode = currentNode.nextNode
            currentNode.nextNode = newNode
            
        self.listLength += 1
    
    def addElementAtPosition(self, elementData, positionIndex: int):
        """
        Inserta un elemento en la posición especificada
        
        Args:
            elementData: Dato a insertar
            positionIndex: Índice de posición (0-based)
            
        Raises:
            IndexError: Si el índice está fuera de rango
        """
        if positionIndex < 0 or positionIndex > self.listLength:
            raise IndexError("Índice fuera de rango")
            
        newNode = Node(elementData)
        
        if positionIndex == 0:
            newNode.nextNode = self.headNode
            self.headNode = newNode
        else:
            currentNode = self.headNode
            for _ in range(positionIndex - 1):
                currentNode = currentNode.nextNode
            newNode.nextNode = currentNode.nextNode
            currentNode.nextNode = newNode
            
        self.listLength += 1
    
    def getElementAtIndex(self, positionIndex: int):
        """
        Obtiene el elemento en la posición especificada
        
        Args:
            positionIndex: Índice de posición (0-based)
            
        Returns:
            Dato almacenado en la posición
            
        Raises:
            IndexError: Si el índice está fuera de rango
        """
        if positionIndex < 0 or positionIndex >= self.listLength:
            raise IndexError("Índice fuera de rango")
            
        currentNode = self.headNode
        for _ in range(positionIndex):
            currentNode = currentNode.nextNode
            
        return currentNode.elementData
    
    def removeElementAtIndex(self, positionIndex: int):
        """
        Elimina el elemento en la posición especificada
        
        Args:
            positionIndex: Índice de posición (0-based)
            
        Returns:
            Dato eliminado
            
        Raises:
            IndexError: Si el índice está fuera de rango
        """
        if positionIndex < 0 or positionIndex >= self.listLength:
            raise IndexError("Índice fuera de rango")
            
        if positionIndex == 0:
            removedData = self.headNode.elementData
            self.headNode = self.headNode.nextNode
        else:
            previousNode = self.headNode
            for _ in range(positionIndex - 1):
                previousNode = previousNode.nextNode
                
            removedData = previousNode.nextNode.elementData
            previousNode.nextNode = previousNode.nextNode.nextNode
            
        self.listLength -= 1
        return removedData
    
    def searchElement(self, targetData):
        """
        Busca un elemento en la lista
        
        Args:
            targetData: Dato a buscar
            
        Returns:
            Índice de la primera ocurrencia o -1 si no se encuentra
        """
        currentNode = self.headNode
        currentIndex = 0
        
        while currentNode:
            if currentNode.elementData == targetData:
                return currentIndex
            currentNode = currentNode.nextNode
            currentIndex += 1
            
        return -1
    
    def isEmpty(self):
        """
        Verifica si la lista está vacía
        
        Returns:
            True si está vacía, False de lo contrario
        """
        return self.listLength == 0
    
    def getListLength(self):
        """
        Devuelve la cantidad de elementos en la lista
        
        Returns:
            Número de elementos
        """
        return self.listLength
    
    def clearList(self):
        """
        Vacía completamente la lista
        """
        self.headNode = None
        self.listLength = 0
    
    def __iter__(self):
        """
        Iterador sobre los elementos de la lista
        
        Yields:
            Elementos de la lista en orden
        """
        currentNode = self.headNode
        while currentNode:
            yield currentNode.elementData
            currentNode = currentNode.nextNode
    
    def __str__(self):
        """
        Representación en cadena de la lista
        
        Returns:
            Cadena con elementos en formato [a -> b -> c]
        """
        elements = []
        currentNode = self.headNode
        while currentNode:
            elements.append(str(currentNode.elementData))
            currentNode = currentNode.nextNode
        return "[" + " -> ".join(elements) + "]" if elements else "Lista Vacía"