from numeros.numero import Number
from core.tiposUtilidades import allElementsMeet  
from ..utilidades.normalizador import normalizeDecimalNumber  
from utilidades.validadores import validateBasicOperation
from errores.tiposErrores import (
    DivisionByZeroError,
    MathematicalIndeterminacyError,
    InvalidNumericOperationError
)

class Decimal(Number):
    def __init__(self, inputValue: str):
        processedValue = inputValue.replace(',', '.').replace(' ', '')
        super().__init__(processedValue)
    
    def determineBase(self) -> int:
        return 10
    
    def isValid(self, value: str) -> bool:
        if value.startswith('-') or value.startswith('+'):
            value = value[1:]
        
        if 'e' in value.lower():
            parts = value.lower().split('e')
            if len(parts) != 2:
                return False
            return self.isValidPart(parts[0]) and self.isValidPart(parts[1])
        
        return self.isValidPart(value)
    
    def isValidPart(self, part: str) -> bool:
        if not part:
            return True
            
        if '.' in part:
            integer, fractional = part.split('.', 1)
            if integer and not allElementsMeet(integer, lambda char: char.isdigit()):
                return False
            if fractional and not allElementsMeet(fractional, lambda char: char.isdigit()):
                return False
            return True
        
        return allElementsMeet(part, lambda char: char.isdigit())
    
    def normalizeValue(self):
        self.normalizedForm = normalizeDecimalNumber(self.originalValue)
    
    def countSignificantDigits(self):
        value = self.originalValue
        
        if value.startswith('-') or value.startswith('+'):
            value = value[1:]
        
        if allElementsMeet(value, lambda char: char in '0.,'):
            self.significantDigits = 1
            return
        
        if 'e' in value.lower():
            mantissa, _ = value.lower().split('e')
            value = mantissa
        
        parts = value.split('.')
        integerPart = parts[0].lstrip('0')
        
        if len(parts) > 1:
            fractionalPart = parts[1].rstrip('0')
        else:
            fractionalPart = ""
        
        significantDigits = integerPart + fractionalPart
        
        if not significantDigits:
            self.significantDigits = 1
        else:
            self.significantDigits = len(significantDigits)
    
    def determineSupportedOperations(self):
        self.supportedOperations = ['+', '-', '*', '/']
    
    def convertToFloat(self) -> float:
        return float(self.originalValue.replace(',', '.'))
    
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
    
    def operate(self, operation: str, other) -> 'Decimal':
        self_val = self.convertToFloat()
        other_val = other.convertToFloat()
        
        try:
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
            
            return Decimal(str(result))
        
        except (DivisionByZeroError, MathematicalIndeterminacyError) as e:
            print(f"Error en operacion {operation}: {str(e)}")
            return None

    def __str__(self) -> str:
        return (f"Decimal: {self.originalValue} | "
                f"Normalizado: {self.normalizedForm} | "
                f"Digitos Significativos: {self.significantDigits} | "
                f"Operaciones: {''.join(self.supportedOperations)}")