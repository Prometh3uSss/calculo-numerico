from listaEnlazada import ListaEnlazada

class Cola:
    def __init__(self):  # Corregido: __init__
        self.datos = ListaEnlazada()
        self.ultimo = None
    
    def encolar(self, elemento):
        nuevo_nodo = Nodo(elemento)
        if not self.datos.cabeza:
            self.datos.cabeza = nuevo_nodo
            self.ultimo = nuevo_nodo
        else:
            self.ultimo.siguiente = nuevo_nodo
            self.ultimo = nuevo_nodo
        self.datos.longitud += 1
    
    def desencolar(self):
        if self.esta_vacia():
            raise IndexError("Cola vacía")
        dato = self.datos.cabeza.dato
        self.datos.cabeza = self.datos.cabeza.siguiente
        self.datos.longitud -= 1
        if self.esta_vacia():
            self.ultimo = None
        return dato
    
    def esta_vacia(self):
        return self.datos.longitud == 0
    
    def frente(self):
        return self.datos.cabeza.dato if not self.esta_vacia() else None