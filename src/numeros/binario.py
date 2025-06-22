from numeros.Number import Number
from utilidades.NumberValidator import isValidBinary
from utilidades.NumberNormalizer import normalizeBinary
from errores.CustomExceptions import InvalidNumberFormatException

class Binary(Number):
    def __init__(self, value: str):
        """
        Inicializa un número binario
        
        Args:
            value: Cadena que representa el número binario
            
        Raises:
            InvalidNumberFormatException: Si el formato no es válido
        """
        # Normalizar formato (quitar espacios, manejar signo)
        processedValue = value.replace(' ', '')
        super().__init__(processedValue)
    
    def determineBase(self) -> int:
        """
        Determina la base numérica (2 para binario)
        
        Returns:
            2
        """
        return 2
    
    def isValid(self, value: str) -> bool:
        """
        Valida si el valor es un número binario válido
        
        Args:
            value: Valor a validar
            
        Returns:
            True si es válido, False en caso contrario
        """
        return isValidBinary(value)
    
    def normalize(self):
        """
        Convierte el número a notación científica binaria
        Ejemplo: "101.01" -> "1.0101 × 2^2"
        """
        self.normalizedForm = normalizeBinary(self.originalValue)
    
    def countSignificantDigits(self):
        """
        Calcula la cantidad de cifras significativas según reglas:
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
        Los números binarios soportan suma, resta y multiplicación
        División solo si el número no es cero
        """
        self.supportedOperations = ['+', '-', '*']
        
        # Verificar si es cero
        if self.originalValue.replace('0', '').replace('.', '') != '':
            self.supportedOperations.append('/')
    
    def toDecimal(self) -> float:
        """
        Convierte el número binario a su valor decimal
        
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
        
        # Dividir en parte entera y fraccionaria
        parts = value.split('.')
        
        # Convertir parte entera
        integerValue = 0
        if parts[0]:
            integerValue = int(parts[0], 2)
        
        # Convertir parte fraccionaria
        fractionalValue = 0.0
        if len(parts) > 1 and parts[1]:
            for i, bit in enumerate(parts[1], 1):
                if bit == '1':
                    fractionalValue += 2 ** (-i)
        
        return sign * (integerValue + fractionalValue)
    
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
        return (f"Binario: {self.originalValue} | "
                f"Normalizado: {self.normalizedForm} | "
                f"Cifras: {self.significantDigits} | "
                f"Operaciones: {''.join(self.supportedOperations)}")