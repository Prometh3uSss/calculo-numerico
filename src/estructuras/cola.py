from listaEnlazada import LinkedList  # Asumiendo que ListaEnlazada se renombró a LinkedList

class Node:
    """Nodo para una lista enlazada"""
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.dataList = LinkedList()
        self.lastNode = None
    
    def enqueue(self, element):
        """
        Agrega un elemento al final de la cola
        
        Args:
            element: Elemento a agregar
        """
        new_node = Node(element)
        if not self.dataList.head:
            self.dataList.head = new_node
            self.lastNode = new_node
        else:
            self.lastNode.next = new_node
            self.lastNode = new_node
        self.dataList.length += 1
    
    def dequeue(self):
        """
        Elimina y devuelve el elemento al frente de la cola
        
        Returns:
            Elemento removido
            
        Raises:
            IndexError: Si la cola está vacía
        """
        if self.isEmpty():
            raise IndexError("Cola vacía")
        data = self.dataList.head.data
        self.dataList.head = self.dataList.head.next
        self.dataList.length -= 1
        if self.isEmpty():
            self.lastNode = None
        return data
    
    def isEmpty(self):
        """
        Verifica si la cola está vacía
        
        Returns:
            bool: True si está vacía, False de lo contrario
        """
        return self.dataList.length == 0
    
    def front(self):
        """
        Obtiene el elemento al frente de la cola sin eliminarlo
        
        Returns:
            Elemento al frente o None si está vacía
        """
        return self.dataList.head.data if not self.isEmpty() else None