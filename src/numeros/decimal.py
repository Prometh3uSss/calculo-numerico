from numero import Numero
from utilidades.normalizador import normalizarDecimal

class Decimal(Numero):
    def _init_(self, valor):
        self.sistema = "Decimal"
        super()._init_(valor)
    
    def validar(self):
        
        pass
    
    def calcularCifrasSignificativas(self):
        valor = self.valor.replace(',', '.')
        if '.' in valor:
            entero, decimal = valor.split('.')
        else:
            entero, decimal = valor, ""
        
        
        entero = entero.lstrip('0')
        decimal = decimal.rstrip('0')
        
        self.cifrasSignificativas = len(entero) + len(decimal)
        if self.cifrasSignificativas == 0:
            self.cifrasSignificativas = 1  
    
    def normalizar(self):
        self.mantisa, self.exponente = normalizarDecimal(self.valor)
    
    def aDecimal(self):
        return float(self.valor.replace(',', '.'))