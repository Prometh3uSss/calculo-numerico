from numeros.numero import Number
from utilidades.normalizador import normalizeBinaryNumber
from errores.tiposErrores import InvalidNumberFormatError
from core.tiposUtilidades import allElementsMeet

class Binary(Number):
    def __init__(self, inputValue: str):
        processedValue = inputValue.replace(' ', '')
        super().__init__(processedValue)
    
    def determineBase(self) -> int:
        return 2
    
    def isValid(self, value: str) -> bool:
        if value.startswith('-') or value.startswith('+'):
            value = value[1:]
        
        parts = value.split('.')
        if len(parts) > 2:
            return False
        
        for part in parts:
            if part:
                if not allElementsMeet(part, lambda char: char in '01'):
                    return False
        return True
    
    def normalizeValue(self):
        self.normalizedForm = normalizeBinaryNumber(self.originalValue)
    
    def countSignificantDigits(self):
        value = self.originalValue
        
        if value.startswith('-') or value.startswith('+'):
            value = value[1:]
        
        if allElementsMeet(value, lambda char: char in '0.,'):
            self.significantDigits = 1
            return
        
        parts = value.split('.')
        integerPart = parts[0].lstrip('0')
        fractionalPart = parts[1].rstrip('0') if len(parts) > 1 else ""
        
        significantDigits = integerPart + fractionalPart
        significantDigits = significantDigits.lstrip('0')
        
        if not significantDigits:
            self.significantDigits = 1 
        else:
            self.significantDigits = len(significantDigits)
    
    def determineSupportedOperations(self):
        self.supportedOperations = ['+', '-', '*']
        
        valueWithoutSign = self.originalValue.replace('-', '').replace('+', '')
        if not allElementsMeet(valueWithoutSign, lambda char: char in '0.,'):
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
    
    def getOriginalValue(self) -> str:
        return self.originalValue
    
    def getNormalizedForm(self) -> str:
        return self.normalizedForm
    
    def getSignificantDigitsCount(self) -> int:
        return self.significantDigits
    
    def getSupportedOperations(self) -> list:
        return self.supportedOperations
    
    def getBase(self) -> int:
        return self.base
    
    def __str__(self) -> str:
        return (f"Binary: {self.originalValue} | "
                f"Normalizado: {self.normalizedForm} | "
                f"Digitos Significativos: {self.significantDigits} | "
                f"Operaciones: {''.join(self.supportedOperations)}")