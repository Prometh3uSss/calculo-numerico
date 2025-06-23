"""
Clase base abstracta para representaciones numéricas
Define interfaz común para Binary, Decimal y Hexadecimal
Cumple con estándar camelCase en inglés y comentarios en español
"""

from abc import ABC, abstractmethod
from errores.tiposErrores import InvalidNumberFormatException

class Number(ABC):
    def __init__(self, inputValue: str):
        """
        Inicializa un número con su valor original y procesa sus propiedades
        
        Args:
            inputValue: Valor numérico en formato cadena
            
        Raises:
            InvalidNumberFormatException: Si el formato es inválido
        """
        if not self.isValid(inputValue):
            raise InvalidNumberFormatException(f"Formato inválido: {inputValue}")
        
        self.originalValue = inputValue
        self.normalizedForm = ""
        self.significantDigits = 0
        self.supportedOperations = []
        self.numericBase = self.determineBase()
        
        self.normalizeValue()
        self.countSignificantDigits()
        self.determineSupportedOperations()
    
    @abstractmethod
    def determineBase(self) -> int:
        """
        Determina la base numérica (2, 10, 16)
        
        Returns:
            Base numérica
        """
        pass
    
    @abstractmethod
    def isValid(self, value: str) -> bool:
        """
        Valida el formato del número según su base
        
        Args:
            value: Valor a validar
            
        Returns:
            True si es válido, False en caso contrario
        """
        pass
    
    @abstractmethod
    def normalizeValue(self):
        """
        Convierte el número a su forma normalizada (notación científica)
        """
        pass
    
    @abstractmethod
    def countSignificantDigits(self):
        """
        Calcula la cantidad de cifras significativas
        """
        pass
    
    @abstractmethod
    def determineSupportedOperations(self):
        """
        Determina las operaciones elementales soportadas (+, -, *, /)
        """
        pass
    
    @abstractmethod
    def convertToDecimal(self) -> float:
        """
        Convierte el número a su equivalente decimal
        
        Returns:
            Valor decimal en punto flotante
        """
        pass
    
    def getOriginalValue(self) -> str:
        """
        Devuelve el valor original del número
        
        Returns:
            Valor original en formato cadena
        """
        return self.originalValue
    
    def getNormalizedForm(self) -> str:
        """
        Devuelve la representación normalizada
        
        Returns:
            Notación científica del número
        """
        return self.normalizedForm
    
    def getSignificantDigitCount(self) -> int:
        """
        Devuelve el número de cifras significativas
        
        Returns:
            Cantidad de cifras significativas
        """
        return self.significantDigits
    
    def getSupportedOperations(self) -> list:
        """
        Devuelve las operaciones soportadas
        
        Returns:
            Lista de operaciones elementales (+, -, *, /)
        """
        return self.supportedOperations
    
    def getNumericBase(self) -> int:
        """
        Devuelve la base numérica
        
        Returns:
            Base del sistema numérico (2, 10, 16)
        """
        return self.numericBase
    
    def __str__(self) -> str:
        """
        Representación legible del número
        
        Returns:
            Cadena descriptiva con propiedades clave
        """
        return (f"Original: {self.originalValue} | "
                f"Base: {self.numericBase} | "
                f"Normalized: {self.normalizedForm} | "
                f"Significant Digits: {self.significantDigits} | "
                f"Operations: {''.join(self.supportedOperations)}")