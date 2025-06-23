from numeros.numero import Number
from utilidades.normalizador import normalizeHexadecimalNumber
from errores.tiposErrores import InvalidNumberFormatError

class Hexadecimal(Number):
    def __init__(self, inputValue: str):
        processedValue = inputValue.upper().replace(' ', '')
        super().__init__(processedValue)
    
    def determineBase(self) -> int:
        return 16
    
    def isValid(self, value: str) -> bool:  # Corregido: Usar nombre de clase base
        # Permitir signo opcional
        if value.startswith('-') or value.startswith('+'):
            value = value[1:]
        
        # Convertir a mayúsculas para validación
        value = value.upper()
        
        # Dividir en parte entera y fraccionaria
        parts = value.split('.')
        if len(parts) > 2:  # Maximo un punto decimal
            return False
        
        validChars = '0123456789ABCDEF'
        for part in parts:
            if part:
                if not all(char in validChars for char in part):
                    return False
        return True
    
    def normalizeValue(self):
        self.normalizedForm = normalizeHexadecimalNumber(self.originalValue)
    
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
        
        # Combinar digitos significativos (sin ceros iniciales/finales)
        significantDigits = integerPart + fractionalPart
        significantDigits = significantDigits.lstrip('0')
        
        if significantDigits == "":
            self.significantDigits = 1  # Caso 0.000
        else:
            self.significantDigits = len(significantDigits)
    
    def determineSupportedOperations(self):
        self.supportedOperations = ['+', '-', '*']
        
        # Permitir division solo si no es cero
        valueWithoutSign = self.originalValue.replace('-', '').replace('+', '')
        if not all(char in '0.' for char in valueWithoutSign):
            self.supportedOperations.append('/')
    
    def convertToFloat(self) -> float:
        sign = -1 if self.originalValue.startswith('-') else 1
        value = self.originalValue.replace('-', '').replace('+', '')
        
        parts = value.split('.')
        integerValue = int(parts[0], 16) if parts[0] else 0
        fractionalValue = 0.0
        
        if len(parts) > 1 and parts[1]:
            for position, hexChar in enumerate(parts[1], 1):
                fractionalValue += int(hexChar, 16) * (16 ** (-position))
        
        return sign * (integerValue + fractionalValue)
    
    # Métodos de acceso (consistentes con clase base)
    def getSignificantDigitsCount(self) -> int:
        return self.significantDigits