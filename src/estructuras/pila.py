from listaEnlazada import LinkedList  # Asumiendo que ListaEnlazada se renombró a LinkedList

class Node:
    """Nodo para una lista enlazada"""
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        """Inicializa una pila vacía"""
        self.dataList = LinkedList()
    
    def push(self, element):
        """
        Apila un elemento en la cima de la pila
        
        Args:
            element: Elemento a apilar
        """
        # Insertar al inicio para O(1)
        newNode = Node(element)
        newNode.next = self.dataList.head
        self.dataList.head = newNode
        self.dataList.length += 1
    
    def pop(self):
        """
        Desapila y devuelve el elemento en la cima de la pila
        
        Returns:
            Elemento desapilado
            
        Raises:
            IndexError: Si la pila está vacía
        """
        if self.isEmpty():
            raise IndexError("Pila vacía")
        data = self.dataList.head.data
        self.dataList.head = self.dataList.head.next
        self.dataList.length -= 1
        return data
    
    def isEmpty(self):
        """
        Verifica si la pila está vacía
        
        Returns:
            bool: True si está vacía, False de lo contrario
        """
        return self.dataList.length == 0
    
    def top(self):
        """
        Obtiene el elemento en la cima de la pila sin desapilarlo
        
        Returns:
            Elemento en la cima o None si está vacía
        """
        return self.dataList.head.data if not self.isEmpty() else None