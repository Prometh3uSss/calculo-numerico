from abc import ABC, abstractmethod

class Numero(ABC):
    def __init__(self, valor):
        self.valor_original = valor
        self.valor_normalizado = ""
        self.cifras_significativas = 0
        self.base = 10
        self.operaciones_posibles = []
    
    @abstractmethod
    def normalizar(self):
        pass
    
    @abstractmethod
    def contar_cifras_significativas(self):
        pass
    
    @abstractmethod
    def determinar_operaciones(self):
        pass
    
    def __str__(self):
        return (f"{self.valor_original} | Base: {self.base} | "
                f"Normalizado: {self.valor_normalizado} | "
                f"Cifras: {self.cifras_significativas} | "
                f"Operaciones: {''.join(self.operaciones_posibles)}")