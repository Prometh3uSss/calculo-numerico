import numpy as np
import random

class Number:
    def __init__(self, value: str):
        """
        Inicializa un número con su valor original y procesa sus propiedades
        
        Args:
            value: Valor original del número como cadena
        """
        self.originalValue = value
        self.bases = np.array([], dtype=int)
        self.normalizedForms = np.array([], dtype=object)
        self.significantDigits = np.array([], dtype=int)
        self.possibleOperations = np.array([], dtype=object)
        self.isValid = True
        self.errorMessage = ""
        self._processValue()
        self._validateNumberSystems()

    def _validateNumberSystems(self):
        """Valida que el número pertenezca a al menos un sistema numérico"""
        if len(self.bases) == 0:
            self.isValid = False
            self.errorMessage = f"Inválido: '{self.originalValue}' no es binario, decimal ni hexadecimal"
    
    def _processValue(self):
        """Procesa el valor para determinar sus propiedades en diferentes bases"""
        valueLower = self.originalValue.lower()
        validBases = []
        if self._isBinary(valueLower):
            validBases.append(2)
        if self._isDecimal(valueLower):
            validBases.append(10)
        if self._isHexadecimal(valueLower):
            validBases.append(16)
        
        self.bases = np.array(validBases, dtype=int)
        forms = []
        digits = []
        operations = []
        
        for base in validBases:
            form = self._calculateNormalizedForm(valueLower, base)
            digitCount = self._countSignificantDigits(valueLower, base)
            ops = self._demonstrateOperationsByComputation(valueLower, base)
            forms.append(form)
            digits.append(digitCount)
            operations.append(ops)
        
        self.normalizedForms = np.array(forms, dtype=object)
        self.significantDigits = np.array(digits, dtype=int)
        self.possibleOperations = np.array(operations, dtype=object)
    
    def _isBinary(self, value: str) -> bool:
        """Verifica si el valor es un número binario válido"""
        pointFound = False
        for char in value:
            if char == '.':
                if pointFound: 
                    return False
                pointFound = True
            elif char not in '01':
                return False
        return True
    
    def _isDecimal(self, value: str) -> bool:
        """Verifica si el valor es un número decimal válido"""
        pointFound = False
        for char in value:
            if char == '.':
                if pointFound:
                    return False
                pointFound = True
            elif not char.isdigit():
                return False
        return True
    
    def _isHexadecimal(self, value: str) -> bool:
        """Verifica si el valor es un número hexadecimal válido"""
        pointFound = False
        for char in value:
            if char == '.':
                if pointFound:
                    return False
                pointFound = True
            elif not (char.isdigit() or 'a' <= char <= 'f'):
                return False
        return True
    
    def _calculateNormalizedForm(self, value: str, base: int) -> str:
        """Calcula la forma normalizada del número para una base dada"""
        pointPosition = value.find('.')
        
        if pointPosition != -1:
            integerPart = value[:pointPosition]
            fractionalPart = value[pointPosition+1:]
        else:
            integerPart = value
            fractionalPart = ""
        
        startIndex = 0
        while startIndex < len(integerPart) and integerPart[startIndex] == '0':
            startIndex += 1
        
        if startIndex >= len(integerPart) and not fractionalPart:
            return "0"
        
        exponent = len(integerPart) - startIndex - 1 if startIndex < len(integerPart) else -1
        
        mantissa = ""
        if startIndex < len(integerPart):
            mantissa = integerPart[startIndex:]
            if fractionalPart:
                mantissa += '.' + fractionalPart
        elif fractionalPart:
            startFraction = 0
            while startFraction < len(fractionalPart) and fractionalPart[startFraction] == '0':
                startFraction += 1
            if startFraction < len(fractionalPart):
                mantissa = fractionalPart[startFraction:]
                exponent = -startFraction - 1
            else:
                return "0"
        else:
            return "0"
        
        return f"{mantissa} × {base}^{exponent}"
    
    def _countSignificantDigits(self, value: str, base: int) -> int:
        """Cuenta las cifras significativas en el número"""
        valueWithoutPoint = value.replace('.', '')
        
        startIndex = 0
        while startIndex < len(valueWithoutPoint) and valueWithoutPoint[startIndex] == '0':
            startIndex += 1
        
        if startIndex == len(valueWithoutPoint):
            return 1  # Caso especial para cero

        return len(valueWithoutPoint) - startIndex

    def _charToInt(self, charDigit: str) -> int:
        """Convierte un carácter a su valor entero según la base"""
        if '0' <= charDigit <= '9':
            return ord(charDigit) - ord('0')
        elif 'a' <= charDigit <= 'f':
            return ord(charDigit) - ord('a') + 10
        return 0 

    def _intToChar(self, intValue: int) -> str:
        """Convierte un valor entero a su representación de carácter"""
        if 0 <= intValue <= 9:
            return chr(ord('0') + intValue)
        elif 10 <= intValue <= 15:
            return chr(ord('a') + intValue - 10)
        return '0' 

    def _padStringsLeft(self, str1: str, str2: str) -> tuple[str, str]:
        """Rellena dos cadenas con ceros a la izquierda para igualar su longitud"""
        maxLen = max(len(str1), len(str2))
        str1Padded = str1.zfill(maxLen)
        str2Padded = str2.zfill(maxLen)
        return str1Padded, str2Padded

    def _removeLeadingZeros(self, numStr: str) -> str:
        """Elimina los ceros a la izquierda de una cadena numérica"""
        return numStr.lstrip('0') or '0'

    def _addStringsManually(self, num1Str: str, num2Str: str, base: int) -> str:
        """Realiza una suma manual de dos cadenas numéricas en una base dada"""
        num1Padded, num2Padded = self._padStringsLeft(num1Str, num2Str)
        result = []
        carry = 0
        for i in range(len(num1Padded) - 1, -1, -1):
            digit1Val = self._charToInt(num1Padded[i])
            digit2Val = self._charToInt(num2Padded[i])
            currentSum = digit1Val + digit2Val + carry
            result.append(self._intToChar(currentSum % base))
            carry = currentSum // base 
        if carry > 0:
            result.append(self._intToChar(carry))
        return self._removeLeadingZeros(''.join(reversed(result)))

    def _isGreaterOrEqual(self, num1Str: str, num2Str: str, base: int) -> bool:
        """Compara dos cadenas numéricas para determinar si num1 >= num2"""
        num1Clean = self._removeLeadingZeros(num1Str)
        num2Clean = self._removeLeadingZeros(num2Str)
        if len(num1Clean) > len(num2Clean):
            return True
        if len(num1Clean) < len(num2Clean):
            return False
        for i in range(len(num1Clean)):
            digit1 = self._charToInt(num1Clean[i])
            digit2 = self._charToInt(num2Clean[i])
            if digit1 > digit2:
                return True
            if digit1 < digit2:
                return False
        return True 

    def _subtractStringsManually(self, num1Str: str, num2Str: str, base: int) -> str:
        """Realiza una resta manual de dos cadenas numéricas en una base dada"""
        if not self._isGreaterOrEqual(num1Str, num2Str, base):
            return "ERROR: Resultado negativo"
        num1Padded, num2Padded = self._padStringsLeft(num1Str, num2Str)
        result = []
        borrow = 0
        for i in range(len(num1Padded) - 1, -1, -1):
            digit1Val = self._charToInt(num1Padded[i])
            digit2Val = self._charToInt(num2Padded[i])
            currentDiff = digit1Val - digit2Val - borrow
            if currentDiff < 0:
                currentDiff += base
                borrow = 1
            else:
                borrow = 0
            result.append(self._intToChar(currentDiff))
        return self._removeLeadingZeros(''.join(reversed(result)))

    def _multiplySingleDigit(self, numStr: str, digitChar: str, base: int) -> str:
        """Multiplica una cadena numérica por un solo dígito en una base dada"""
        digitVal = self._charToInt(digitChar)
        result = []
        carry = 0
        for i in range(len(numStr) - 1, -1, -1):
            product = self._charToInt(numStr[i]) * digitVal + carry 
            result.append(self._intToChar(product % base))
            carry = product // base
        if carry > 0:
            result.append(self._intToChar(carry))
        return ''.join(reversed(result))

    def _multiplyStringsManually(self, num1Str: str, num2Str: str, base: int) -> str:
        """Realiza una multiplicación manual de dos cadenas numéricas en una base dada"""
        partialProducts = []
        for i in range(len(num2Str) - 1, -1, -1):
            productLine = self._multiplySingleDigit(num1Str, num2Str[i], base)
            for _ in range(len(num2Str) - 1 - i):
                productLine += '0'
            partialProducts.append(productLine)
        finalSum = '0'
        for product in partialProducts:
            finalSum = self._addStringsManually(finalSum, product, base)
        return finalSum

    def _divideStringsManually(self, num1Str: str, num2Str: str, base: int) -> str:
        """Realiza una división manual de dos cadenas numéricas en una base dada"""
        if num2Str == '0':
            raise ZeroDivisionError("División por cero")
        num1Clean = self._removeLeadingZeros(num1Str)
        num2Clean = self._removeLeadingZeros(num2Str)
        if num1Clean == '0':
            return '0'
        if not self._isGreaterOrEqual(num1Clean, num2Clean, base):
            return '0'
        
        quotient = "0"
        currentDividend = "" 
        for digitChar in num1Clean:
            currentDividend += digitChar
            currentDividend = self._removeLeadingZeros(currentDividend)
            currentQuotientDigit = 0
            while self._isGreaterOrEqual(currentDividend, num2Clean, base):
                currentDividend = self._subtractStringsManually(currentDividend, num2Clean, base)
                currentQuotientDigit += 1
            quotient += self._intToChar(currentQuotientDigit)
        return self._removeLeadingZeros(quotient)

    def _isValidNumber(self, numStr: str, base: int) -> bool:
        """Verifica si una cadena es un número válido para una base dada"""
        validChars = {
            2: '01',
            10: '0123456789',
            16: '0123456789abcdef'
        }.get(base, '')
        return all(char in validChars for char in numStr)

    def _demonstrateOperationsByComputation(self, valueStr: str, base: int) -> str:
        """Determina las operaciones posibles mediante cálculo con un número aleatorio"""
        if '.' in valueStr:
            return "" 
        
        randomDigit = random.randint(1, 9)
        operandStr = ""
        if base == 10:
            operandStr = str(randomDigit)
        else:
            tempVal = randomDigit
            while tempVal > 0:
                operandStr = self._intToChar(tempVal % base) + operandStr
                tempVal = tempVal // base
        
        possibleOperations = []
        try:
            sumResult = self._addStringsManually(valueStr, operandStr, base)
            if self._isValidNumber(sumResult, base):
                possibleOperations.append('+')
        except:
            pass
        try:
            subtractResult = self._subtractStringsManually(valueStr, operandStr, base)
            if not subtractResult.startswith("ERROR:") and self._isValidNumber(subtractResult, base):
                possibleOperations.append('-')
        except:
            pass
        try:
            multiplyResult = self._multiplyStringsManually(valueStr, operandStr, base)
            if self._isValidNumber(multiplyResult, base):
                possibleOperations.append('*')
        except:
            pass
        try:
            if operandStr != '0':
                divideResult = self._divideStringsManually(valueStr, operandStr, base)
                if self._isValidNumber(divideResult, base):
                    possibleOperations.append('/')
        except:
            pass
        return ''.join(possibleOperations)

    def getCompleteResult(self) -> str:
        """Devuelve una cadena con todos los resultados del procesamiento del número"""
        if not self.isValid:
            return f"{self.originalValue} | {self.errorMessage}"
        
        output = f"{self.originalValue}"
        for i in range(len(self.bases)):
            output += (
                f"|Base:{self.bases[i]}"
                f"|Forma:{self.normalizedForms[i]}"
                f"|Cifras:{self.significantDigits[i]}"
                f"|Operaciones:{self.possibleOperations[i]}"
            )
        return output

# Ejemplos de uso
num = Number("10")
print(num.getCompleteResult())
num = Number("1010")
print(num.getCompleteResult())