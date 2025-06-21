from abc import ABC, abstractmethod
from utilidades.validadores import validarFormatoNumero

class Numero(ABC):
    def _init_(self, valor):
        self.valor = valor
        self.sistema = ""
        self.cifrasSignificativas = 0
        self.mantisa = ""
        self.exponente = 0
        
        
        validarFormatoNumero(valor, self.sistema)
        
        self.validar()
        self.calcularCifrasSignificativas()
        self.normalizar()
    
    @property
    def valor(self):
        return self.valor
    
    @property
    def sistema(self):
        return self.sistema
    
    @property
    def cifrasSignificativas(self):
        return self.cifrasSignificativas
    
    @property
    def mantisa(self):
        return self.mantisa
    
    @property
    def exponente(self):
        return self.exponente
    
    @abstractmethod
    def validar(self):
        pass
    
    @abstractmethod
    def calcularCifrasSignificativas(self):
        pass
    
    @abstractmethod
    def normalizar(self):
        pass
    
    @abstractmethod
    def aDecimal(self):
        pass
    
    def formaNormalizada(self):
        return f"{self.mantisa} × {self.sistema[0].lower()}^{self.exponente}"
    
    def operacionesPosibles(self):
        return ["Suma", "Resta", "Multiplicacion", "Division"]