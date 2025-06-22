class Node:
    def __init__(self, data):
        """
        Inicializa un nodo con un dato
        
        Args:
            data: Dato a almacenar en el nodo
        """
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        """Inicializa una lista enlazada vacía"""
        self.head = None
        self.length = 0

    def append(self, data):
        """
        Agrega un nuevo elemento al final de la lista
        
        Args:
            data: Dato a agregar
        """
        newNode = Node(data)
        if not self.head:
            self.head = newNode
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = newNode
        self.length += 1

    def get(self, index):
        """
        Obtiene el elemento en la posición especificada
        
        Args:
            index: Índice del elemento a obtener
            
        Returns:
            Elemento en la posición indicada
            
        Raises:
            IndexError: Si el índice está fuera de rango
        """
        if index < 0 or index >= self.length:
            raise IndexError("Índice fuera de rango")
        current = self.head
        for _ in range(index):
            current = current.next
        return current.data

    def __len__(self):
        """
        Devuelve la longitud de la lista
        
        Returns:
            Número de elementos en la lista
        """
        return self.length

    def __iter__(self):
        """
        Iterador sobre los elementos de la lista
        
        Yields:
            Elementos de la lista en orden
        """
        current = self.head
        while current:
            yield current.data
            current = current.next