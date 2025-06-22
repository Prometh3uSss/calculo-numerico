from numeros.Number import Number
from utilidades.NumberValidator import isValidDecimal
from utilidades.NumberNormalizer import normalizeDecimal
from errores.CustomExceptions import InvalidNumberFormatException

class Decimal(Number):
    def __init__(self, value: str):
        """
        Inicializa un número decimal
        
        Args:
            value: Cadena que representa el número decimal
            
        Raises:
            InvalidNumberFormatException: Si el formato no es válido
        """
        # Normalizar comas a puntos y quitar espacios
        processedValue = value.replace(',', '.').replace(' ', '')
        super().__init__(processedValue)
    
    def determineBase(self) -> int:
        """
        Determina la base numérica (10 para decimal)
        
        Returns:
            10
        """
        return 10
    
    def isValid(self, value: str) -> bool:
        """
        Valida si el valor es un número decimal válido
        
        Args:
            value: Valor a validar
            
        Returns:
            True si es válido, False en caso contrario
        """
        return isValidDecimal(value)
    
    def normalize(self):
        """
        Convierte el número a notación científica decimal
        Ejemplo: "123.45" -> "1.2345 × 10^2"
        """
        self.normalizedForm = normalizeDecimal(self.originalValue)
    
    def countSignificantDigits(self):
        """
        Calcula la cantidad de cifras significativas según reglas matemáticas:
        - Los ceros a la izquierda no son significativos
        - Los ceros entre dígitos o a la derecha son significativos
        - Los ceros finales después del punto son significativos
        """
        value = self.originalValue
        
        # Manejar signo
        if value.startswith('-') or value.startswith('+'):
            value = value[1:]
        
        # Caso especial: cero
        if all(c in '0.,' for c in value):
            self.significantDigits = 1
            return
        
        # Dividir en parte entera y decimal
        parts = value.split('.')
        integerPart = parts[0].lstrip('0')  # Quitar ceros a la izquierda
        
        if len(parts) > 1:
            decimalPart = parts[1].rstrip('0')  # Quitar ceros a la derecha
        else:
            decimalPart = ""
        
        # Contar cifras significativas
        if integerPart:
            self.significantDigits = len(integerPart) + len(decimalPart)
        else:
            # Buscar primer dígito no cero en decimal
            for i, char in enumerate(decimalPart):
                if char != '0':
                    self.significantDigits = len(decimalPart) - i
                    return
            self.significantDigits = 1
    
    def determineSupportedOperations(self):
        """
        Determina las operaciones elementales posibles
        Los números decimales soportan todas las operaciones básicas
        """
        self.supportedOperations = ['+', '-', '*', '/']
    
    def toDecimal(self) -> float:
        """
        Convierte el número decimal a su valor flotante
        
        Returns:
            Valor numérico en punto flotante
        """
        # Manejar signo
        sign = 1
        if self.originalValue.startswith('-'):
            sign = -1
            value = self.originalValue[1:]
        elif self.originalValue.startswith('+'):
            value = self.originalValue[1:]
        else:
            value = self.originalValue
        
        # Convertir a flotante
        try:
            return sign * float(value)
        except ValueError:
            # Manejar casos especiales de formato
            value = value.replace(',', '.')
            return sign * float(value)
    
    def getOriginalValue(self) -> str:
        return self.originalValue
    
    def getNormalizedForm(self) -> str:
        return self.normalizedForm
    
    def getSignificantDigitCount(self) -> int:
        return self.significantDigits
    
    def getSupportedOperations(self) -> list:
        return self.supportedOperations
    
    def getBase(self) -> int:
        return self.base
    
    def __str__(self) -> str:
        return (f"Decimal: {self.originalValue} | "
                f"Normalizado: {self.normalizedForm} | "
                f"Cifras: {self.significantDigits} | "
                f"Operaciones: {''.join(self.supportedOperations)}")