import numpy as np
import random 

class Numero:
    def __init__(self, valor: str):
        self.valor_original = valor
        self.bases = np.array([], dtype=int)
        self.formas_normalizadas = np.array([], dtype=object)
        self.cifras_significativas = np.array([], dtype=int)
        self.operaciones_posibles = np.array([], dtype=object)
        self.es_valido = True
        self.mensaje_error = ""
        
        self._procesar_valor()
        self._validar_sistemas_numericos()

    def _validar_sistemas_numericos(self):
        if len(self.bases) == 0:
            self.es_valido = False
            self.mensaje_error = f"Invalido: '{self.valor_original}' no es binario, decimal ni hexadecimal"
    
    def _procesar_valor(self):
        valor = self.valor_original.lower()
        
        bases_validas = []
        if self._es_binario(valor):
            bases_validas.append(2)
        if self._es_decimal(valor):
            bases_validas.append(10)
        if self._es_hexadecimal(valor):
            bases_validas.append(16)
        
        self.bases = np.array(bases_validas, dtype=int)
        
        formas = []
        cifras = []
        operaciones = []
        
        for base in bases_validas:
            forma = self._calcular_forma_normalizada(valor, base)
            cifra = self._contar_cifras_significativas(valor, base)
            
            formas.append(forma)
            cifras.append(cifra)
            
            if base == 10:
                ops = self._demostrar_operaciones_decimal(valor)
                operaciones.append(ops)
            else:
                operaciones.append("") 
        
        self.formas_normalizadas = np.array(formas, dtype=object)
        self.cifras_significativas = np.array(cifras, dtype=int)
        self.operaciones_posibles = np.array(operaciones, dtype=object)
    
    def _es_binario(self, valor: str) -> bool:
        return all(c in '01.' for c in valor)
    
    def _es_decimal(self, valor: str) -> bool:
        partes = valor.split('.')
        if len(partes) > 2:
            return False
        return all(part.isdigit() for part in partes)
    
    def _es_hexadecimal(self, valor: str) -> bool:
        return all(c in '0123456789abcdef.' for c in valor)
    
    def _calcular_forma_normalizada(self, valor: str, base: int) -> str:
        if '.' in valor:
            partes = valor.split('.')
            entera = partes[0]
            decimal = partes[1]
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
            if inicio + 1 < len(entera) or decimal:
                mantisa += '.' + entera[inicio+1:] + decimal
        elif decimal:
            inicio_dec = 0
            while inicio_dec < len(decimal) and decimal[inicio_dec] == '0':
                inicio_dec += 1
            if inicio_dec < len(decimal):
                mantisa = decimal[inicio_dec] + '.' + decimal[inicio_dec+1:]
                exponente = -inicio_dec - 1
            else:
                return "0"
        else:
            return "0"
        
        return f"{mantisa} × {base}^{exponente}"
    
    def _contar_cifras_significativas(self, valor: str, base: int) -> int:
        if valor.startswith('-'):
            valor = valor[1:]

        if '.' in valor:
            valor_sin_punto = valor.replace('.', '')
            
            inicio_significativo = 0
            while inicio_significativo < len(valor_sin_punto) and valor_sin_punto[inicio_significativo] == '0':
                inicio_significativo += 1
            
            if inicio_significativo == len(valor_sin_punto):
                return 1

            if '.' in self.valor_original:
                return len(valor_sin_punto) - inicio_significativo
            else:
                return len(valor.lstrip('0'))
        else:
            valor_sin_ceros_izquierda = valor.lstrip('0')
            
            if not valor_sin_ceros_izquierda:
                return 1

            return len(valor_sin_ceros_izquierda)

    def _demostrar_operaciones_decimal(self, valor: str) -> str:
        operaciones = []
        
        try:
            num_original = float(valor) if '.' in valor else int(valor)
        except ValueError:
            return ""

        # Generar un operando aleatorio entre 2 y 9
        operando_aleatorio = random.randint(2, 9) 
            
        # Asegurarse de que operando_aleatorio no sea 0 si se va a usar para división
        if operando_aleatorio == 0: # Aunque random.randint(2,9) nunca dará 0, es buena práctica defensiva.
            operando_aleatorio = 1 

        # Las operaciones manuales usan el operando aleatorio
        try:
            resultado_suma = self._suma_manual(num_original, operando_aleatorio)
            operaciones.append(f"{num_original} + {operando_aleatorio} = {resultado_suma:.4f}")
        except Exception:
            pass
        
        try:
            resultado_resta = self._resta_manual(num_original, operando_aleatorio)
            operaciones.append(f"{num_original} - {operando_aleatorio} = {resultado_resta:.4f}")
        except Exception:
            pass
        
        try:
            resultado_multiplicacion = self._multiplicacion_manual(num_original, operando_aleatorio)
            operaciones.append(f"{num_original} * {operando_aleatorio} = {resultado_multiplicacion:.4f}")
        except Exception:
            pass
        
        try:
            if operando_aleatorio != 0:
                resultado_division = self._division_manual(num_original, operando_aleatorio)
                operaciones.append(f"{num_original} / {operando_aleatorio} = {resultado_division:.4f}")
            else:
                operaciones.append(f"{num_original} / {operando_aleatorio} = División por cero")
        except ZeroDivisionError:
            operaciones.append(f"{num_original} / {operando_aleatorio} = División por cero")
        except Exception:
            pass
        
        return " | ".join(operaciones)
    
    def _suma_manual(self, a, b):
        """Suma computacional mediante incrementos sucesivos para enteros, o suma directa para flotantes."""
        if isinstance(a, float) or isinstance(b, float):
            return a + b # Si hay flotantes, usar suma nativa para precisión.
        
        result = a
        if b > 0:
            for _ in range(b):
                result += 1
        else:
            for _ in range(abs(b)):
                result -= 1
        return result
    
    def _resta_manual(self, a, b):
        """Resta computacional mediante decrementos sucesivos para enteros, o resta directa para flotantes."""
        if isinstance(a, float) or isinstance(b, float):
            return a - b # Si hay flotantes, usar resta nativa para precisión.
        
        result = a
        if b > 0:
            for _ in range(b):
                result -= 1
        else:
            for _ in range(abs(b)):
                result += 1
        return result
    
    def _multiplicacion_manual(self, a, b):
        """Multiplicación computacional mediante sumas sucesivas para enteros, o multiplicación directa para flotantes."""
        if isinstance(a, float) or isinstance(b, float):
            return a * b # Si hay flotantes, usar multiplicación nativa.

        result = 0
        sign = 1
        if a < 0:
            sign *= -1
            a = abs(a)
        if b < 0:
            sign *= -1
            b = abs(b)

        for _ in range(b): # Este bucle solo es viable para 'b' entero y pequeño
            result = self._suma_manual(result, a) # Recursión con _suma_manual, que ahora es eficiente
        
        return result * sign
    
    def _division_manual(self, a, b):
        """División computacional mediante restas sucesivas para enteros, o división directa para flotantes."""
        if b == 0:
            raise ZeroDivisionError("División por cero no es posible.")
        
        if isinstance(a, float) or isinstance(b, float):
            return a / b # Si hay flotantes, usar división nativa.

        sign = 1
        if a < 0:
            sign *= -1
            a = abs(a)
        if b < 0:
            sign *= -1
            b = abs(b)
        
        contador = 0
        temp_a = a
        # Este bucle solo es viable si a/b es un entero pequeño
        while temp_a >= b: 
            temp_a = self._resta_manual(temp_a, b) # Recursión con _resta_manual, que ahora es eficiente
            contador += 1
        
        return contador * sign
    
    def resultado_completo(self) -> str:
        if not self.es_valido:
            return f"{self.valor_original} | {self.mensaje_error}"
        
        salida = f"{self.valor_original}"
        
        for i in range(len(self.bases)):
            salida += (
                f"|Base:{self.bases[i]}"
                f"|Forma:{self.formas_normalizadas[i]}"
                f"|Cifras:{self.cifras_significativas[i]}"
                f"|Operaciones:{self.operaciones_posibles[i]}"
            )
        
        return salida
num = Numero("0.0050")
print(num.resultado_completo())