import numpy as np

class Numero:
    def __init__(self, valor: str):
        self.valor_original = valor
        self.bases = np.array([], dtype=int)
        self.formas_normalizadas = np.array([], dtype=object)
        self.cifras_significativas = np.array([], dtype=int)
        self.operaciones_posibles = np.array([], dtype=object)

        self._procesar_valor()
        
    
    def _procesar_valor(self):
        """Procesa el valor y determina propiedades mediante computación real"""
        valor = self.valor_original.lower().replace(',', '.')
        
        # Determinar bases válidas
        bases_validas = []
        if self._es_binario(valor):
            bases_validas.append(2)
        if self._es_decimal(valor):
            bases_validas.append(10)
        if self._es_hexadecimal(valor):
            bases_validas.append(16)
        
        self.bases = np.array(bases_validas, dtype=int)
        
        # Procesar cada base válida
        formas = []
        cifras = []
        operaciones = []
        
        for base in bases_validas:
            # Calcular propiedades básicas
            forma = self._calcular_forma_normalizada(valor, base)
            cifra = self._contar_cifras_significativas(valor, base)
            decimal = self._convertir_a_decimal(valor, base)
            
            formas.append(forma)
            cifras.append(cifra)
            
            # DEMOSTRAR operaciones posibles mediante computación real
            ops = self._demostrar_operaciones(valor, base, decimal)
            operaciones.append(ops)
        
        self.formas_normalizadas = np.array(formas, dtype=object)
        self.cifras_significativas = np.array(cifras, dtype=int)
        self.operaciones_posibles = np.array(operaciones, dtype=object)
    
    def _es_binario(self, valor: str) -> bool:
        return all(c in '01.' for c in valor)
    
    def _es_decimal(self, valor: str) -> bool:
        return all(c in '0123456789.' for c in valor)
    
    def _es_hexadecimal(self, valor: str) -> bool:
        return all(c in '0123456789abcdef.' for c in valor)
    
    def _calcular_forma_normalizada(self, valor: str, base: int) -> str:
        """Calcula la forma normalizada para una base específica"""
        if valor.replace('.', '') == '0' * len(valor.replace('.', '')):
            return "0"
        
        inicio = 0
        while inicio < len(valor) and valor[inicio] in '0.':
            inicio += 1
        
        if inicio >= len(valor):
            return "0"
        
        parte_entera = valor.split('.')[0]
        exponente = len(parte_entera) - inicio - 1 if inicio < len(parte_entera) else -1
        
        mantisa = valor[inicio]
        resto = valor[inicio+1:].replace('.', '')
        if resto:
            mantisa += '.' + resto
        
        return f"{mantisa} × {base}^{exponente}"
    
    def _contar_cifras_significativas(self, valor: str, base: int) -> int:
        valor_limpio = valor.strip('0').replace('.', '')
        return len(valor_limpio) if valor_limpio else 0
    
    def _convertir_a_decimal(self, valor: str, base: int) -> float:
        """Convierte a decimal para operaciones de demostración"""
        partes = valor.split('.')
        entera = partes[0] or '0'
        decimal = partes[1] if len(partes) > 1 else ''
        
        total = 0
        for digito in entera:
            total = total * base + int(digito, base)
        
        factor = 1 / base
        for digito in decimal:
            total += int(digito, base) * factor
            factor /= base
        
        return total
    
    def _demostrar_operaciones(self, valor: str, base: int, decimal: float) -> str:
        """DEMOSTRACIÓN COMPUTACIONAL de operaciones posibles"""
        operaciones = []
        operando_prueba = "10"  # Número genérico para pruebas
        
        # 1. Suma: valor + 10 (en misma base)
        try:
            resultado_suma = self._sumar_en_base(valor, operando_prueba, base)
            operaciones.append('+')
        except:
            pass
        
        # 2. Resta: valor - 10 (en misma base)
        try:
            resultado_resta = self._restar_en_base(valor, operando_prueba, base)
            operaciones.append('-')
        except:
            pass
        
        # 3. Multiplicación: valor * 10 (en misma base)
        try:
            resultado_mult = self._multiplicar_en_base(valor, operando_prueba, base)
            operaciones.append('*')
        except:
            pass
        
        # 4. División: valor / 10 (en misma base)
        try:
            if float(decimal) != 0:  # Evitar división por cero
                resultado_div = self._dividir_en_base(valor, operando_prueba, base)
                operaciones.append('/')
        except:
            pass
        
        return ''.join(operaciones)
    
    def _sumar_en_base(self, num1: str, num2: str, base: int) -> str:
        """Realiza suma real en la base especificada"""
        # Convertir a decimal, sumar, y convertir de vuelta
        dec1 = self._convertir_a_decimal(num1, base)
        dec2 = self._convertir_a_decimal(num2, base)
        suma_dec = dec1 + dec2
        return self._convertir_de_base(suma_dec, base)
    
    def _restar_en_base(self, num1: str, num2: str, base: int) -> str:
        """Realiza resta real en la base especificada"""
        dec1 = self._convertir_a_decimal(num1, base)
        dec2 = self._convertir_a_decimal(num2, base)
        resta_dec = dec1 - dec2
        return self._convertir_de_base(resta_dec, base)
    
    def _multiplicar_en_base(self, num1: str, num2: str, base: int) -> str:
        """Realiza multiplicación real en la base especificada"""
        dec1 = self._convertir_a_decimal(num1, base)
        dec2 = self._convertir_a_decimal(num2, base)
        mult_dec = dec1 * dec2
        return self._convertir_de_base(mult_dec, base)
    
    def _dividir_en_base(self, num1: str, num2: str, base: int) -> str:
        """Realiza división real en la base especificada"""
        dec1 = self._convertir_a_decimal(num1, base)
        dec2 = self._convertir_a_decimal(num2, base)
        div_dec = dec1 / dec2
        return self._convertir_de_base(div_dec, base)
    
    def _convertir_de_base(self, decimal: float, base: int) -> str:
        """Convierte un número decimal a la base especificada"""
        if decimal == 0:
            return "0"
        
        # Parte entera
        parte_entera = abs(int(decimal))
        entera_str = ""
        while parte_entera > 0:
            resto = parte_entera % base
            entera_str = self._digito(resto) + entera_str
            parte_entera //= base
        
        # Parte decimal
        parte_decimal = abs(decimal) - int(abs(decimal))
        decimal_str = ""
        precision = 10  # Precisión máxima para evitar bucles infinitos
        
        while parte_decimal > 0 and precision > 0:
            parte_decimal *= base
            digito = int(parte_decimal)
            decimal_str += self._digito(digito)
            parte_decimal -= digito
            precision -= 1
        
        # Construir resultado
        resultado = entera_str or "0"
        if decimal_str:
            resultado += '.' + decimal_str
        
        return resultado
    
    def _digito(self, valor: int) -> str:
        """Convierte dígitos >9 a letras para hexadecimal"""
        if valor < 10:
            return str(valor)
        return chr(ord('a') + valor - 10)
    
    def resultado_completo(self) -> str:
        salida = f"{self.valor_original}"
        
        if len(self.bases) == 0:
            return f"Invalido: '{self.valor_original}' no es binario, decimal ni hexadecimal"
        
        for i in range(len(self.bases)):
            salida += (
                f"|Base:{self.bases[i]}"
                f"|Forma:{self.formas_normalizadas[i]}"
                f"|Cifras:{self.cifras_significativas[i]}"
                f"|Operaciones:{self.operaciones_posibles[i]}"
            )
        
        return salida
num = Numero("z%")
print(num.resultado_completo())
    
    