from listaEnlazada import ListaEnlazada

class Pila:
    def __init__(self):  # Corregido: __init__
        self.datos = ListaEnlazada()
    
    def apilar(self, elemento):
        # Insertar al inicio para O(1)
        nuevo_nodo = Nodo(elemento)
        nuevo_nodo.siguiente = self.datos.cabeza
        self.datos.cabeza = nuevo_nodo
        self.datos.longitud += 1
    
    def desapilar(self):
        if self.esta_vacia():
            raise IndexError("Pila vacía")
        dato = self.datos.cabeza.dato
        self.datos.cabeza = self.datos.cabeza.siguiente
        self.datos.longitud -= 1
        return dato
    
    def esta_vacia(self):
        return self.datos.longitud == 0
    
    def cima(self):
        return self.datos.cabeza.dato if not self.esta_vacia() else None