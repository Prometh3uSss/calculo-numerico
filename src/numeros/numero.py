from abc import ABC, abstractmethod

class Number(ABC):
    def __init__(self, value):
        self.originalValue = value
        self.normalizedValue = ""
        self.significantDigits = 0
        self.base = 10
        self.possibleOperations = []
    
    @abstractmethod
    def normalize(self):
        """Convierte el número a notación científica"""
        pass
    
    @abstractmethod
    def countSignificantDigits(self):
        """Calcula la cantidad de cifras significativas"""
        pass
    
    @abstractmethod
    def determinePossibleOperations(self):
        """Determina las operaciones posibles para el número"""
        pass
    
    def __str__(self):
        return (f"{self.originalValue} | Base: {self.base} | "
                f"Normalizado: {self.normalizedValue} | "
                f"Cifras: {self.significantDigits} | "
                f"Operaciones: {''.join(self.possibleOperations)}")