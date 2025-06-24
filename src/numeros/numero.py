from abc import ABC, abstractmethod
from errores.tiposErrores import InvalidNumberFormatError

class Number(ABC):
    def __init__(self, inputValue: str):
        if type(inputValue).__name__ != 'str':
            raise InvalidNumberFormatError("Tipo de entrada no valido")
        if not self.isValid(inputValue):
            raise InvalidNumberFormatError(f"Formato invalido: {inputValue}")
        
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
        pass
    
    @abstractmethod
    def isValid(self, value: str) -> bool:
        pass
    
    @abstractmethod
    def normalizeValue(self):
        pass
    
    @abstractmethod
    def countSignificantDigits(self):
        pass
    
    @abstractmethod
    def determineSupportedOperations(self):
        pass
    
    @abstractmethod
    def convertToFloat(self) -> float:
        pass
    
    def getOriginalValue(self) -> str:
        return self.originalValue
    
    def getNormalizedForm(self) -> str:
        return self.normalizedForm
    
    def getSignificantDigitsCount(self) -> int:
        return self.significantDigits
    
    def getSupportedOperations(self) -> list:
        return self.supportedOperations
    
    def getNumericBase(self) -> int:
        return self.numericBase
    
    def __str__(self) -> str:
        return (f"Original: {self.originalValue} | "
                f"Base: {self.numericBase} | "
                f"Normalizado: {self.normalizedForm} | "
                f"Digitos Significativos: {self.significantDigits} | "
                f"Operaciones: {''.join(self.supportedOperations)}")