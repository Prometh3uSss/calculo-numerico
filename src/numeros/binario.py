from numeros.numero import Number
from utilidades.normalizador import normalizeBinaryNumber
from errores.tiposErrores import InvalidNumberFormatError

class Binary(Number):
    def __init__(self, inputValue: str):
        processedValue = inputValue.replace(' ', '')
        super().__init__(processedValue)
    
    def determineBase(self) -> int:
        return 2
    
    def isValid(self, value: str) -> bool:
        # Permitir signo opcional
        if value.startswith('-') or value.startswith('+'):
            value = value[1:]
        
        # Dividir en parte entera y fraccionaria
        parts = value.split('.')
        if len(parts) > 2:  # Maximo un punto decimal
            return False
        
        # Cada parte debe contener solo 0 y 1
        for part in parts:
            if part and not all(char in '01' for char in part):
                return False
        return True
    
    def normalizeValue(self):  # Corregido: Nombre requerido por clase base
        self.normalizedForm = normalizeBinaryNumber(self.originalValue)
    
    def countSignificantDigits(self):
        value = self.originalValue
        
        # Manejar signo
        if value.startswith('-') or value.startswith('+'):
            value = value[1:]
        
        # Caso especial: cero
        if all(char in '0.' for char in value):
            self.significantDigits = 1
            return
        
        # Dividir en parte entera y fraccionaria
        parts = value.split('.')
        integerPart = parts[0].lstrip('0')
        fractionalPart = parts[1] if len(parts) > 1 else ""
        
        # Combinar digitos significativos
        significantDigits = integerPart + fractionalPart
        significantDigits = significantDigits.lstrip('0')
        
        if significantDigits == "":
            self.significantDigits = 1  # Caso 0.000
        else:
            self.significantDigits = len(significantDigits)
    
    def determineSupportedOperations(self):
        """Binarios soportan +, -, *, / (excepto división por cero)"""
        self.supportedOperations = ['+', '-', '*']
        
        # Permitir division solo si no es cero
        # Verificar si el valor es cero: si después de quitar signo y puntos, solo hay ceros
        valueWithoutSign = self.originalValue.replace('-', '').replace('+', '')
        if not all(char in '0.' for char in valueWithoutSign):
            self.supportedOperations.append('/')
    
    def convertToFloat(self) -> float:
        sign = -1 if self.originalValue.startswith('-') else 1
        value = self.originalValue.replace('-', '').replace('+', '')
        
        parts = value.split('.')
        integerValue = int(parts[0], 2) if parts[0] else 0
        fractionalValue = 0.0
        
        if len(parts) > 1 and parts[1]:
            for position, bit in enumerate(parts[1], 1):
                if bit == '1':
                    fractionalValue += 2 ** (-position)
        
        return sign * (integerValue + fractionalValue)

    def getSignificantDigitsCount(self) -> int:
        return self.significantDigits