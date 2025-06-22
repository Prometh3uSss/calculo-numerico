from numero import Number  # Asumiendo que Numero se renombró a Number

class Binary(Number):
    def validate(self):
        """Valida que el valor sea un binario válido"""
        if not all(char in '01.' for char in self.value):
            raise ValueError(f"Valor '{self.value}' no es binario válido")
        self.system = "Binario"
    
    def calculateSignificantDigits(self):
        """Calcula la cantidad de cifras significativas en el número binario"""
        parts = self.value.split('.')
        if len(parts) == 1:
            self.significantDigits = len(parts[0].lstrip('0'))
        else:
            integerDigits = len(parts[0].lstrip('0'))
            fractionalDigits = len(parts[1].rstrip('0'))
            self.significantDigits = integerDigits + fractionalDigits
    
    def toDecimal(self):
        """Convierte el número binario a decimal"""
        parts = self.value.split('.')
        integerPart = int(parts[0], 2) if parts[0] else 0
        fractionalPart = 0
        
        if len(parts) > 1 and parts[1]:
            for index, bit in enumerate(parts[1]):
                fractionalPart += int(bit) * 2**(-index-1)
        
        return integerPart + fractionalPart
    
    def getNormalizedForm(self):
        """Devuelve la forma normalizada en notación científica binaria"""
        decimalValue = self.toDecimal()
        if decimalValue == 0:
            return "0"
        
        exponent = 0
        num = abs(decimalValue)
        
        # Normalizar el número
        while num >= 2:
            num /= 2
            exponent += 1
        while num < 1:
            num *= 2
            exponent -= 1
        
        sign = "-" if decimalValue < 0 else ""
        return f"{sign}{num:.4f} × 2^{exponent}"