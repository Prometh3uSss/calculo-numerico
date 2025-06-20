from .listaEnlazada import ListaEnlazada

class Cola:
    def _init_(self):
        self.datos = ListaEnlazada()
    
    def encolar(self, elemento):
        self.datos.agregar(elemento)
    
    def desencolar(self):
        if self.estaVacia():
            raise IndexError("Cola vacia")
        
        dato = self.datos.cabeza.dato
        self.datos.cabeza = self.datos.cabeza.siguiente
        self.datos.longitud -= 1
        return dato
    
    def estaVacia(self):
        return len(self.datos) == 0
    
    def frente(self):
        if self.estaVacia():
            return None
        return self.datos.obtener(0)