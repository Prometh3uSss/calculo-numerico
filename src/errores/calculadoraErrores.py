class ErrorCalculator:
    @staticmethod
    def calculateAbsoluteError(exactValue: float, approximateValue: float) -> float:
        return abs(exactValue - approximateValue)
    
    @staticmethod
    def calculateRelativeError(exactValue: float, approximateValue: float) -> float:
        if exactValue == 0:
            if approximateValue == 0:
                return 0.0
            return float('inf')
        return abs(exactValue - approximateValue) / abs(exactValue)
    
    @staticmethod
    def calculateRoundingError(significantDigits: int) -> float:
        return 0.5 * 10 ** (-significantDigits)
    
    @staticmethod
    def calculateTruncationError(significantDigits: int) -> float:
        return 10 ** (-significantDigits)
    
    @staticmethod
    def calculateSumErrorPropagation(*errorValues: float) -> float:
        return sum(errorValues)
    
    @staticmethod
    def calculateProductErrorPropagation(values: list[float], absoluteErrors: list[float]) -> float:
        relativeErrorSquaredSum = 0.0
        for i in range(len(values)):
            if values[i] == 0:
                raise ZeroDivisionError("No se puede calcular error relativo para valor cero")
            relativeError = absoluteErrors[i] / abs(values[i])
            relativeErrorSquaredSum += relativeError ** 2
        
        productMagnitude = 1.0
        for value in values:
            productMagnitude *= abs(value)
        
        return productMagnitude * (relativeErrorSquaredSum ** 0.5)