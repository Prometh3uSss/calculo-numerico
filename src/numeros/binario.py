from numeros.numero import Number
from core.tiposUtilidades import allElementsMeet
from ..utilidades.normalizador import normalizeBinaryNumber  
from utilidades.validadores import validateBasicOperation
from errores.tiposErrores import (
    DivisionByZeroError,
    MathematicalIndeterminacyError,
    InvalidNumericOperationError
)

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
    
    def operate(self, operation: str, other) -> 'Binary':
        self_val = self.convertToFloat()
        other_val = other.convertToFloat()
        
        try:
            # Validación antes de operar
            validateBasicOperation(operation, self_val, other_val)

            # Reemplazo de match con if-elif
            if operation == '+':
                result = self_val + other_val
            elif operation == '-':
                result = self_val - other_val
            elif operation == '*':
                result = self_val * other_val
            elif operation == '/':
                result = self_val / other_val
            else:
                raise InvalidNumericOperationError(f"Operacion no soportada: {operation}")
            
            return Binary(str(result))
        
        except (DivisionByZeroError, MathematicalIndeterminacyError) as e:
            print(f"Error en operacion {operation}: {str(e)}")
            return None
    
    def __str__(self) -> str:
        return (f"Binary: {self.originalValue} | "
                f"Normalizado: {self.normalizedForm} | "
                f"Digitos Significativos: {self.significantDigits} | "
                f"Operaciones: {''.join(self.supportedOperations)}")