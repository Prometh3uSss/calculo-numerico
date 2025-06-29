from estructuras.listaEnlazada import LinkedList

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
        return abs(exactValue - approximateValue) / abs(exactValue) #r
    
    @staticmethod
    def calculateRoundingError(significantDigits: int) -> float:
        return 0.5 * 10 ** (-significantDigits)
    
    @staticmethod
    def calculateTruncationError(significantDigits: int) -> float:
        return 10 ** (-significantDigits)
    
    @staticmethod
    def calculateSumErrorPropagation(errorValues: LinkedList) -> float:
        total = 0.0
        current = errorValues.headNode
        while current:
            total += current.elementData
            current = current.nextNode
        return total
    
    @staticmethod
    def calculateProductErrorPropagation(values: LinkedList, absoluteErrors: LinkedList) -> float:
        relativeErrorSquaredSum = 0.0
        current_val = values.headNode
        current_err = absoluteErrors.headNode
        
        if values.getListLength() != absoluteErrors.getListLength():
            raise ValueError("Las listas de valores y errores deben tener la misma longitud")
        
        while current_val and current_err:
            value = current_val.elementData
            abs_error = current_err.elementData
            
            if value == 0:
                if abs_error != 0:
                    relativeError = float('inf')
                else:
                    relativeError = 0.0
            else:
                relativeError = abs_error / abs(value)
            
            relativeErrorSquaredSum += relativeError ** 2
            
            current_val = current_val.nextNode
            current_err = current_err.nextNode
        
        productMagnitude = 1.0
        current = values.headNode
        while current:
            if current.elementData != 0:
                productMagnitude *= abs(current.elementData)
            current = current.nextNode
        
        if relativeErrorSquaredSum == float('inf'):
            return float('inf')
        
        return productMagnitude * (relativeErrorSquaredSum ** 0.5)
