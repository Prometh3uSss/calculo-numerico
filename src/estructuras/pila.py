# Proyecto_Calculo_Numerico/src/estructuras/pila.py
from .lista_enlazada import ListaEnlazada

class Pila:
    def _init_(self):
        self.datos = ListaEnlazada()
    
    def apilar(self, elemento):
        self.datos.agregar(elemento)
    
    def desapilar(self):
        if self.esta_vacia():
            raise IndexError("Pila vacía")
        
        if len(self.datos) == 1:
            dato = self.datos.obtener(0)
            self.datos = ListaEnlazada()
            return dato
        
        actual = self.datos.cabeza
        for _ in range(len(self.datos) - 2):
            actual = actual.siguiente
        dato = actual.siguiente.dato
        actual.siguiente = None
        self.datos.longitud -= 1
        return dato
    
    def esta_vacia(self):
        return len(self.datos) == 0
    
    def cima(self):
        if self.esta_vacia():
            return None
        return self.datos.obtener(len(self.datos) - 1)