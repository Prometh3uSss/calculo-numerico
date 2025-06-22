from .numero import Number  
from ..utilidades.normalizador import normalizeDecimal 

class Decimal(Number):
    def __init__(self, value: str):
        # Preprocesar valor (reemplazar comas por puntos)
        processedValue = self._normalizeFormat(value)
        super().__init__(processedValue)
        self.base = 10
        self.normalize()
        self.countSignificantDigits()
        self.determinePossibleOperations()
    
    def _normalizeFormat(self, value: str) -> str:
        """Convierte comas en puntos y elimina espacios"""
        return value.replace(',', '.').replace(' ', '')
    
    def normalize(self):
        """Convierte el número a notación científica"""
        self.normalizedValue = normalizeDecimal(self.originalValue)
    
    def countSignificantDigits(self):
        """Calcula la cantidad de cifras significativas según reglas matemáticas"""
        value = self.originalValue
        
        # Manejar signo
        if value.startswith('-') or value.startswith('+'):
            value = value[1:]
        
        # Caso especial: cero
        if all(char == '0' for char in value.replace('.', '')):
            self.significantDigits = 1
            return
        
        # Dividir en parte entera y decimal
        parts = value.split('.')
        integerPart = parts[0].lstrip('0')
        
        if len(parts) > 1:
            fractionalPart = parts[1].rstrip('0')
        else:
            fractionalPart = ""
        
        # Contar cifras significativas
        if integerPart:
            self.significantDigits = len(integerPart) + len(fractionalPart)
        else:
            # Buscar primer dígito no cero en decimal
            for index, char in enumerate(fractionalPart):
                if char != '0':
                    self.significantDigits = len(fractionalPart) - index
                    return
            self.significantDigits = 1
    
    def determinePossibleOperations(self):
        """Todas las operaciones son posibles para números decimales"""
        self.possibleOperations = ['+', '-', '*', '/']
    
    def __str__(self):
        return (f"{self.originalValue} | Base: {self.base} | "
                f"Normalizado: {self.normalizedValue} | "
                f"Cifras: {self.significantDigits} | "
                f"Operaciones: {''.join(self.possibleOperations)}")