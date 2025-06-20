import numpy as np
import random 

class Numero:
    def __init__(self, valor: str):
        self.valorOriginal = valor
        self.bases = np.array([], dtype=int)
        self.formasNormalizadas = np.array([], dtype=object)
        self.cifrasSignificativas = np.array([], dtype=int)
        self.operacionesPosibles = np.array([], dtype=object)
        self.esValido = True
        self.mensajeError = ""
        
        self.procesarValor()
        self.validarSistemasNumericos()

    def validarSistemasNumericos(self):
        if len(self.bases) == 0:
            self.esValido = False
            self.mensajeError = f"Invalido: '{self.valorOriginal}' no es binario, decimal ni hexadecimal"
    
    def procesarValor(self):
        valor = self.valorOriginal.lower()
        
        basesValidas = []
        if self.esBinario(valor):
            basesValidas.append(2)
        if self.esDecimal(valor):
            basesValidas.append(10)
        if self.esHexadecimal(valor):
            basesValidas.append(16)
        
        self.bases = np.array(basesValidas, dtype=int)
        
        formas = []
        cifras = []
        operaciones = []
        
        for base in basesValidas:
            forma = self.calcularFormaNormalizada(valor, base)
            cifra = self.contarCifrasSignificativas(valor, base)
            
            formas.append(forma)
            cifras.append(cifra)
            
            opsDemostrablesSimbolos = self.demostrarOperacionesPorComputo(valor, base)
            operaciones.append(opsDemostrablesSimbolos)
        
        self.formasNormalizadas = np.array(formas, dtype=object)
        self.cifrasSignificativas = np.array(cifras, dtype=int)
        self.operacionesPosibles = np.array(operaciones, dtype=object)
    
    def esBinario(self, valor: str) -> bool:
        tienePunto = False
        for char in valor:
            if char == '.':
                if tienePunto: return False 
                tienePunto = True
            elif char not in '01':
                return False
        return True
    
    def esDecimal(self, valor: str) -> bool:
        tienePunto = False
        for char in valor:
            if char == '.':
                if tienePunto: return False 
                tienePunto = True
            elif char not in '0123456789':
                return False
        return True
    
    def esHexadecimal(self, valor: str) -> bool:
        tienePunto = False
        for char in valor:
            if char == '.':
                if tienePunto: return False 
                tienePunto = True
            elif char not in '0123456789abcdef':
                return False
        return True
    
    def calcularFormaNormalizada(self, valor: str, base: int) -> str:
        puntoIndice = -1
        for i in range(len(valor)):
            if valor[i] == '.':
                puntoIndice = i
                break
        
        if puntoIndice != -1:
            entera = valor[0:puntoIndice]
            decimal = valor[puntoIndice+1:]
        else:
            entera = valor
            decimal = ""
        
        inicio = 0
        while inicio < len(entera) and entera[inicio] == '0':
            inicio += 1
        
        if inicio >= len(entera) and not decimal:
            return "0"
        
        exponente = len(entera) - inicio - 1 if inicio < len(entera) else -1
        
        if inicio < len(entera):
            mantisa = entera[inicio]
            for i in range(inicio + 1, len(entera)):
                mantisa += entera[i]
            if decimal:
                mantisa += '.'
                for char in decimal:
                    mantisa += char
        elif decimal:
            inicioDec = 0
            while inicioDec < len(decimal) and decimal[inicioDec] == '0':
                inicioDec += 1
            if inicioDec < len(decimal):
                mantisa = decimal[inicioDec]
                for i in range(inicioDec + 1, len(decimal)):
                    mantisa += decimal[i]
                exponente = -inicioDec - 1
            else:
                return "0"
        else:
            return "0"
        
        return f"{mantisa} x {base}^{exponente}"
    
    def contarCifrasSignificativas(self, valor: str, base: int) -> int:
        esNegativo = False
        if len(valor) > 0 and valor[0] == '-':
            esNegativo = True
            valorProcesado = ""
            for i in range(1, len(valor)):
                valorProcesado += valor[i]
        else:
            valorProcesado = valor

        valorSinPunto = ""
        tienePunto = False
        for char in valorProcesado:
            if char == '.':
                tienePunto = True
            else:
                valorSinPunto += char
            
        inicioSignificativo = 0
        while inicioSignificativo < len(valorSinPunto) and valorSinPunto[inicioSignificativo] == '0':
            inicioSignificativo += 1
        
        if inicioSignificativo == len(valorSinPunto):
            return 1 

        if tienePunto: 
            return len(valorSinPunto) - inicioSignificativo
        else: 
            valorSinCerosIzquierda = ""
            encontroDigitoNoCero = False
            for char in valorProcesado:
                if char != '0':
                    encontroDigitoNoCero = True
                if encontroDigitoNoCero:
                    valorSinCerosIzquierda += char
            
            if not valorSinCerosIzquierda:
                return 1 
            
            return len(valorSinCerosIzquierda)

    def charAInt(self, charDigit: str) -> int:
        """Convierte un caracter digito (0-9, a-f) a su valor entero"""
        if '0' <= charDigit <= '9':
            return ord(charDigit) - ord('0')
        elif 'a' <= charDigit <= 'f':
            return ord(charDigit) - ord('a') + 10
        return 0 

    def intAChar(self, intVal: int) -> str:
        """Convierte un valor entero (0-15) a su caracter digito (0-9, A-F)"""
        if 0 <= intVal <= 9:
            return chr(ord('0') + intVal)
        elif 10 <= intVal <= 15:
            return chr(ord('a') + intVal - 10)
        return '0' 

    def padStringsIzquierda(self, s1: str, s2: str, padChar='0') -> tuple[str, str]:
        """Rellena con un caracter a la izquierda para igualar longitudes"""
        maxLen = len(s1) if len(s1) > len(s2) else len(s2)
        paddedS1 = padChar * (maxLen - len(s1)) + s1
        paddedS2 = padChar * (maxLen - len(s2)) + s2
        return paddedS1, paddedS2

    def eliminarCerosIzquierda(self, numStr: str) -> str:
        """Elimina ceros a la izquierda de una cadena numerica"""
        if len(numStr) == 0:
            return '0'
        idx = 0
        while idx < len(numStr) - 1 and numStr[idx] == '0':
            idx += 1
        return numStr[idx:]

    def sumarCadenasManual(self, num1Str: str, num2Str: str, base: int) -> str:
        """Suma dos numeros representados como cadenas en una base dada"""
        num1Padded, num2Padded = self.padStringsIzquierda(num1Str, num2Str)
        
        result = []
        carry = 0
        
        for i in range(len(num1Padded) - 1, -1, -1):
            digit1Val = self.charAInt(num1Padded[i])
            digit2Val = self.charAInt(num2Padded[i])
            
            currentSum = digit1Val + digit2Val + carry
            digitResult = currentSum % base
            carry = currentSum // base 
            
            result.append(self.intAChar(digitResult))
            
        if carry > 0:
            result.append(self.intAChar(carry))
            
        final_result = "".join(reversed(result))
        return self.eliminarCerosIzquierda(final_result)

    def esMayorOIgual(self, num1Str: str, num2Str: str, base: int) -> bool:
        """Compara si num1Str es mayor o igual que num2Str en una base dada"""
        num1Cleaned = self.eliminarCerosIzquierda(num1Str)
        num2Cleaned = self.eliminarCerosIzquierda(num2Str)

        len1 = len(num1Cleaned)
        len2 = len(num2Cleaned)

        if len1 > len2:
            return True
        if len1 < len2:
            return False

        for i in range(len1):
            digit1 = self.charAInt(num1Cleaned[i])
            digit2 = self.charAInt(num2Cleaned[i])
            if digit1 > digit2:
                return True
            if digit1 < digit2:
                return False
        
        return True 

    def restarCadenasManual(self, num1Str: str, num2Str: str, base: int) -> str:
        """Resta dos numeros representados como cadenas en una base dada (num1 - num2).
           Asume num1 >= num2. No maneja negativos
        """
        if not self.esMayorOIgual(num1Str, num2Str, base):
            return "ERROR: Resultado negativo (no soportado)"
        
        num1Padded, num2Padded = self.padStringsIzquierda(num1Str, num2Str)
        
        result = []
        borrow = 0
        
        for i in range(len(num1Padded) - 1, -1, -1):
            digit1Val = self.charAInt(num1Padded[i])
            digit2Val = self.charAInt(num2Padded[i])
            
            currentDiff = digit1Val - digit2Val - borrow
            
            if currentDiff < 0:
                currentDiff += base
                borrow = 1
            else:
                borrow = 0
            
            result.append(self.intAChar(currentDiff))
            
        finalResult = "".join(reversed(result))
        return self.eliminarCerosIzquierda(finalResult)

    def multiplicarUnDigito(self, numStr: str, digitChar: str, base: int) -> str:
        """Multiplica una cadena numerica por un solo digito en la misma base"""
        if digitChar == '0':
            return '0'
        
        digitVal = self.charAInt(digitChar)
        
        result = []
        carry = 0
        
        for i in range(len(numStr) - 1, -1, -1):
            numDigitVal = self.charAInt(numStr[i])
            product = numDigitVal * digitVal + carry 
            
            resultDigit = product % base
            carry = product // base
            
            result.append(self.intAChar(resultDigit))
            
        if carry > 0:
            result.append(self.intAChar(carry))
            
        return "".join(reversed(result))

    def multiplicarCadenasManual(self, num1Str: str, num2Str: str, base: int) -> str:
        """Multiplica dos numeros representados como cadenas en una base dada"""
        if num1Str == '0' or num2Str == '0':
            return '0'
        
        num1Str = self.eliminarCerosIzquierda(num1Str)
        num2Str = self.eliminarCerosIzquierda(num2Str)

        partialProducts = []
        
        for i in range(len(num2Str) - 1, -1, -1):
            digit2Char = num2Str[i]
            productLine = self.multiplicarUnDigito(num1Str, digit2Char, base)
            
            for _ in range(len(num2Str) - 1 - i):
                productLine += '0'
            
            partialProducts.append(productLine)
        
        finalSum = '0'
        for pProd in partialProducts:
            finalSum = self.sumarCadenasManual(finalSum, pProd, base)
            
        return self.eliminarCerosIzquierda(finalSum)

    def dividirCadenasManual(self, num1Str: str, num2Str: str, base: int) -> str:
        """Divide dos numeros representados como cadenas en una base dada (num1 / num2)
           Devuelve solo la parte entera del cociente
           Requiere implementacion de resta y comparacion de cadenas
        """
        if num2Str == '0':
            raise ZeroDivisionError("Division por cero no es posible")

        num1Str = self.eliminarCerosIzquierda(num1Str)
        num2Str = self.eliminarCerosIzquierda(num2Str)
        
        if num1Str == '0':
            return '0'
        
        if not self.esMayorOIgual(num1Str, num2Str, base):
            return '0'

        cociente = "0"
        dividendoActual = "" 
        
        for digitChar in num1Str:
            dividendoActual += digitChar
            dividendoActual = self.eliminarCerosIzquierda(dividendoActual) 
            
            currentQDigit = 0
            while self.esMayorOIgual(dividendoActual, num2Str, base):
                dividendoActual = self.restarCadenasManual(dividendoActual, num2Str, base)
                tempInc = self.sumarCadenasManual(self.intAChar(currentQDigit), '1', base)
                currentQDigit = self.charAInt(tempInc) 
                if len(tempInc) > 1: 
                    pass 

            cociente += self.intAChar(currentQDigit)
            
        return self.eliminarCerosIzquierda(cociente)

    def demostrarOperacionesPorComputo(self, valorStr: str, base: int) -> str:
        operacionesPosibles = []
        
        operandoDecInt = random.randint(1, 9)

        operandoStr = ""
        tempVal = operandoDecInt
        if base == 10:
            operandoStr = str(operandoDecInt) 
        else: 
            if tempVal == 0:
                operandoStr = '0'
            else:
                while tempVal > 0:
                    remainder = tempVal % base
                    operandoStr = self.intAChar(remainder) + operandoStr
                    tempVal = tempVal // base 
        
        if '.' in valorStr:
            return "" 
        
        try:
            self.sumarCadenasManual(valorStr, operandoStr, base)
            operacionesPosibles.append('+')
        except Exception:
            pass

        try:
            if self.esMayorOIgual(valorStr, operandoStr, base):
                self.restarCadenasManual(valorStr, operandoStr, base)
                operacionesPosibles.append('-')
        except Exception:
            pass
        
        try:
            self.multiplicarCadenasManual(valorStr, operandoStr, base)
            operacionesPosibles.append('*')
        except Exception:
            pass
        
        try:
            if operandoStr != '0': 
                self.dividirCadenasManual(valorStr, operandoStr, base)
                operacionesPosibles.append('/')
            else:
                pass 
        except ZeroDivisionError:
            pass
        except Exception:
            pass
        
        return "".join(operacionesPosibles)
    def resultadoCompleto(self) -> str:
        if not self.esValido:
            return f"{self.valorOriginal} | {self.mensajeError}"
        
        salida = f"{self.valorOriginal}"
        
        for i in range(len(self.bases)):
            salida += (
                f"|Base:{self.bases[i]}"
                f"|Forma:{self.formasNormalizadas[i]}"
                f"|Cifras:{self.cifrasSignificativas[i]}"
                f"|Operaciones:{self.operacionesPosibles[i]}"
            )
        
        return salida

num = Numero("10")
print(num.resultadoCompleto())
num = Numero("1010")
print(num.resultadoCompleto())