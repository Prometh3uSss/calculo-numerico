"""
Clase base abstracta para representaciones numéricas
Define la interfaz común para Binario, Decimal y Hexadecimal
"""

from abc import ABC, abstractmethod
from errores.CustomExceptions import InvalidNumberFormatException

class Number(ABC):
    def __init__(self, value: str):
        """
        Inicializa un número con su valor original
        
        Args:
            value: Valor numérico en cadena
        """
        if not self.isValid(value):
            raise InvalidNumberFormatException(f"Formato inválido: {value}")
        
        self.originalValue = value
        self.normalizedForm = ""
        self.significantDigits = 0
        self.supportedOperations = []
        self.base = self.determineBase()
        
        self.normalize()
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
    def normalize(self):
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
    def toDecimal(self) -> float:
        """
        Convierte el número a su equivalente decimal
        
        Returns:
            Valor decimal
        """
        pass
    
    def getOriginalValue(self) -> str:
        """
        Devuelve el valor original del número
        
        Returns:
            Valor original
        """
        return self.originalValue
    
    def getNormalizedForm(self) -> str:
        """
        Devuelve la forma normalizada
        
        Returns:
            Representación en notación científica
        """
        return self.normalizedForm
    
    def getSignificantDigitCount(self) -> int:
        """
        Devuelve la cantidad de cifras significativas
        
        Returns:
            Número de cifras significativas
        """
        return self.significantDigits
    
    def getSupportedOperations(self) -> list:
        """
        Devuelve las operaciones soportadas
        
        Returns:
            Lista de operaciones (+, -, *, /)
        """
        return self.supportedOperations
    
    def getBase(self) -> int:
        """
        Devuelve la base numérica
        
        Returns:
            Base (2, 10, 16)
        """
        return self.base
    
    def __str__(self) -> str:
        """
        Representación en cadena del número
        
        Returns:
            Cadena descriptiva
        """
        return (f"Valor: {self.originalValue} | "
                f"Base: {self.base} | "
                f"Normalizado: {self.normalizedForm} | "
                f"Cifras Signif: {self.significantDigits} | "
                f"Operaciones: {''.join(self.supportedOperations)}")