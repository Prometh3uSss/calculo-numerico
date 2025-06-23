class ErrorCalculator:
    @staticmethod
    def calculateAbsoluteError(exactValue: float, approximateValue: float) -> float:
        """
        Calcula el error absoluto entre un valor exacto y uno aproximado.
        
        Args:
            exactValue: Valor exacto o de referencia
            approximateValue: Valor aproximado o calculado
            
        Returns:
            Diferencia absoluta entre los valores
        """
        return abs(exactValue - approximateValue)
    
    @staticmethod
    def calculateRelativeError(exactValue: float, approximateValue: float) -> float:
        """
        Calcula el error relativo entre un valor exacto y uno aproximado.
        
        Args:
            exactValue: Valor exacto o de referencia
            approximateValue: Valor aproximado o calculado
            
        Returns:
            Error relativo como fracción del valor exacto
            Infinito si exactValue es 0 y approximateValue ≠ 0
            0 si ambos valores son 0
            
        Raises:
            ZeroDivisionError: Si exactValue es 0 y approximateValue ≠ 0
        """
        if exactValue == 0:
            if approximateValue == 0:
                return 0.0
            return float('inf')
        return abs(exactValue - approximateValue) / abs(exactValue)
    
    @staticmethod
    def calculateRoundingError(significantDigits: int) -> float:
        """
        Calcula el máximo error posible por redondeo para un número de dígitos significativos.
        
        Args:
            significantDigits: Número de dígitos significativos
            
        Returns:
            Error máximo de redondeo: 0.5 × 10^(-significantDigits)
        """
        return 0.5 * 10 ** (-significantDigits)
    
    @staticmethod
    def calculateTruncationError(significantDigits: int) -> float:
        """
        Calcula el máximo error posible por truncamiento para un número de dígitos significativos.
        
        Args:
            significantDigits: Número de dígitos significativos
            
        Returns:
            Error máximo de truncamiento: 10^(-significantDigits)
        """
        return 10 ** (-significantDigits)
    
    @staticmethod
    def calculateSumErrorPropagation(*errorValues: float) -> float:
        """
        Calcula el error propagado al sumar valores con errores individuales.
        
        Args:
            *errorValues: Errores absolutos de cada valor
            
        Returns:
            Suma de los errores absolutos
        """
        return sum(errorValues)
    
    @staticmethod
    def calculateProductErrorPropagation(values: list[float], absoluteErrors: list[float]) -> float:
        """
        Calcula el error propagado al multiplicar valores con errores individuales.
        
        Args:
            values: Valores exactos
            absoluteErrors: Errores absolutos de cada valor
            
        Returns:
            Error propagado absoluto para el producto
            
        Raises:
            ZeroDivisionError: Si algún valor es cero
        """
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