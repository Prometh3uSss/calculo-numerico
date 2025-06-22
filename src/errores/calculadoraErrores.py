class ErrorCalculator:
    @staticmethod
    def absoluteError(exactValue, approximateValue):
        return abs(exactValue - approximateValue)
    
    @staticmethod
    def relativeError(exactValue, approximateValue):
        if exactValue == 0:
            return float('inf') if approximateValue != 0 else 0
        return abs(exactValue - approximateValue) / abs(exactValue)
    
    @staticmethod
    def roundingError(value, significantDigits):
        return 0.5 * 10 ** (-significantDigits)
    
    @staticmethod
    def truncationError(value, significantDigits):
        return 10 ** (-significantDigits)
    
    @staticmethod
    def sumPropagationError(*errors):
        return sum(errors)
    
    @staticmethod
    def productPropagationError(values, errors):
        total = 0
        for i in range(len(values)):
            if values[i] == 0:
                return float('inf')
            total += (errors[i] / abs(values[i])) ** 2
        return abs(values[0] * values[1]) * total ** 0.5