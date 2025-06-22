"""
Implementación optimizada de una estructura de pila (LIFO) usando nodos enlazados
Cumple con los requisitos de usar estructuras propias y nomenclatura camelCase
"""

class Node:
    def __init__(self, data):
        """
        Nodo básico para la pila
        
        Args:
            data: Dato a almacenar en el nodo
        """
        self.data = data
        self.next = None


class Stack:
    def __init__(self):
        """
        Inicializa una pila vacía
        """
        self.top = None  # Referencia al tope de la pila
        self.size = 0    # Contador de elementos
    
    def push(self, element):
        """
        Agrega un elemento al tope de la pila
        
        Args:
            element: Elemento a agregar
        """
        new_node = Node(element)
        new_node.next = self.top
        self.top = new_node
        self.size += 1
    
    def pop(self):
        """
        Remueve y devuelve el elemento en el tope de la pila
        
        Returns:
            Elemento en el tope
            
        Raises:
            IndexError: Si la pila está vacía
        """
        if self.isEmpty():
            raise IndexError("Stack is empty")
        
        data = self.top.data
        self.top = self.top.next
        self.size -= 1
        return data
    
    def peek(self):
        """
        Devuelve el elemento en el tope sin removerlo
        
        Returns:
            Elemento en el tope o None si está vacía
        """
        return self.top.data if self.top else None
    
    def isEmpty(self):
        """
        Verifica si la pila está vacía
        
        Returns:
            True si está vacía, False en caso contrario
        """
        return self.size == 0
    
    def getSize(self):
        """
        Devuelve el número de elementos en la pila
        
        Returns:
            Número de elementos
        """
        return self.size
    
    def clear(self):
        """
        Vacía completamente la pila
        """
        self.top = None
        self.size = 0
    
    def __str__(self):
        """
        Representación en cadena de la pila
        
        Returns:
            Cadena con los elementos de la pila
        """
        elements = []
        current = self.top
        while current:
            elements.append(str(current.data))
            current = current.next
        return "Stack: [" + " <- ".join(elements) + "]" if elements else "Empty Stack"
