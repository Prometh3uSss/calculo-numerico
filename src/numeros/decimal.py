from numeros.numero import Number
from utilidades.normalizador import normalizeDecimalNumber
from errores.tiposErrores import InvalidNumberFormatError

class Decimal(Number):
    def __init__(self, inputValue: str):
        processedValue = inputValue.replace(',', '.').replace(' ', '')
        super().__init__(processedValue)
    
    def determineBase(self) -> int:
        return 10
    
    def isValid(self, value: str) -> bool:
        # Permitir signo opcional
        if value.startswith('-') or value.startswith('+'):
            value = value[1:]
        
        # Casos especiales: notacion cientifica
        if 'e' in value.lower():
            parts = value.lower().split('e')
            if len(parts) != 2:
                return False
            return all(self.isValidPart(p) for p in parts)
        
        return self.isValidPart(value)
    
    def isValidPart(self, part: str) -> bool:
        if '.' in part:
            integer, fractional = part.split('.', 1)
            return integer.isdigit() and fractional.isdigit()
        return part.isdigit()
    
    def normalizeValue(self):
        self.normalizedForm = normalizeDecimalNumber(self.originalValue)
    
    def countSignificantDigits(self):
        value = self.originalValue
        
        # Manejar signo
        if value.startswith('-') or value.startswith('+'):
            value = value[1:]
        
        # Caso especial: cero
        if value.replace('0', '').replace('.', '') == '':
            self.significantDigits = 1
            return
        
        # Manejar notacion cientifica
        if 'e' in value.lower():
            mantissa, _ = value.lower().split('e')
            value = mantissa
        
        # Dividir en parte entera y fraccionaria
        parts = value.split('.')
        integerPart = parts[0].lstrip('0')
        
        if len(parts) > 1:
            fractionalPart = parts[1].rstrip('0')
        else:
            fractionalPart = ""
        
        # Combinar digitos significativos
        significantDigits = integerPart + fractionalPart
        
        if significantDigits == "":
            self.significantDigits = 1
        else:
            self.significantDigits = len(significantDigits)
    
    def determineSupportedOperations(self):
        self.supportedOperations = ['+', '-', '*', '/']
    
    def convertToFloat(self) -> float:
        return float(self.originalValue.replace(',', '.'))
    
    def getSignificantDigitsCount(self) -> int:
        return self.significantDigits