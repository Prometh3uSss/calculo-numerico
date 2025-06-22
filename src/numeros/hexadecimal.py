from numero import Numero

class Hexadecimal(Numero):
    def validate(self):
        """Valida que el valor sea hexadecimal"""
        if not all(char in '0123456789abcdefABCDEF.' for char in self.value):
            raise ValueError(f"Valor '{self.value}' no es hexadecimal valido")
        self.system = "Hexadecimal"
    
    def calculateSignificantDigits(self):
        """Calcula cifras significativas"""
        parts = self.value.split('.')
        if len(parts) == 1:
            self.significantDigits = len(parts[0].lstrip('0'))
        else:
            self.significantDigits = len(parts[0].lstrip('0')) + len(parts[1].rstrip('0'))
    
    def toDecimal(self):
        """Convierte a decimal"""
        parts = self.value.split('.')
        integerPart = int(parts[0], 16) if parts[0] else 0
        fractionalPart = 0
        if len(parts) > 1 and parts[1]:
            fractionalPart = sum(int(char, 16) * 16**(-index-1) for index, char in enumerate(parts[1]))
        return integerPart + fractionalPart
    
    def getNormalizedForm(self):
        """Devuelve forma normalizada"""
        decimalValue = self.toDecimal()
        if decimalValue == 0:
            return "0"
        
        exponent = 0
        num = abs(decimalValue)
        while num >= 16:
            num /= 16
            exponent += 1
        while num < 1:
            num *= 16
            exponent -= 1
        
        sign = "-" if decimalValue < 0 else ""
        return f"{sign}{num:.4f} × 16^{exponent}"