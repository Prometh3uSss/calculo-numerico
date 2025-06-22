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
            ops = self._demostrar_operaciones_por_computo(valor, base)
            formas.append(forma)
            cifras.append(cifra)
            operaciones.append(ops)
        
        self.formas_normalizadas = np.array(formas, dtype=object)
        self.cifras_significativas = np.array(cifras, dtype=int)
        self.operaciones_posibles = np.array(operaciones, dtype=object)
    
    def _es_binario(self, valor: str) -> bool:
        i = 0
        punto = False
        while i < len(valor):
            char = valor[i]
            if char == '.':
                if punto: 
                    return False
                punto = True
            elif not (char == '0' or char == '1'):
                return False
            i += 1
        return True
    
    def _es_decimal(self, valor: str) -> bool:
        i = 0
        punto = False
        while i < len(valor):
            char = valor[i]
            if char == '.':
                if punto:
                    return False
                punto = True
            elif not (char >= '0' and char <= '9'):
                return False
            i += 1
        return True
    
    def _es_hexadecimal(self, valor: str) -> bool:
        i = 0
        punto = False
        while i < len(valor):
            char = valor[i]
            if char == '.':
                if punto:
                    return False
                punto = True
            elif not ((char >= '0' and char <= '9') or (char >= 'a' and char <= 'f')):
                return False
            i += 1
        return True
    
    def _calcular_forma_normalizada(self, valor: str, base: int) -> str:
        punto_pos = -1
        for i in range(len(valor)):
            if valor[i] == '.':
                punto_pos = i
                break
        
        if punto_pos != -1:
            entera = valor[:punto_pos]
            decimal = valor[punto_pos+1:]
        else:
            entera = valor
            decimal = ""
        
        inicio = 0
        while inicio < len(entera) and entera[inicio] == '0':
            inicio += 1
        
        if inicio >= len(entera) and len(decimal) == 0:
            return "0"
        
        exponente = len(entera) - inicio - 1 if inicio < len(entera) else -1
        
        mantisa = ""
        if inicio < len(entera):
            mantisa = entera[inicio:]
            if len(decimal) > 0:
                mantisa += '.' + decimal
        elif len(decimal) > 0:
            inicio_dec = 0
            while inicio_dec < len(decimal) and decimal[inicio_dec] == '0':
                inicio_dec += 1
            if inicio_dec < len(decimal):
                mantisa = decimal[inicio_dec:]
                exponente = -inicio_dec - 1
            else:
                return "0"
        else:
            return "0"
        
        return f"{mantisa} x {base}^{exponente}"
    
    def _contar_cifras_significativas(self, valor: str, base: int) -> int:
        valor_sin_punto = []
        for char in valor:
            if char != '.':
                valor_sin_punto.append(char)
        
        inicio = 0
        while inicio < len(valor_sin_punto) and valor_sin_punto[inicio] == '0':
            inicio += 1
        
        if inicio == len(valor_sin_punto):
            return 1 

        if '.' in valor:
            return len(valor_sin_punto) - inicio
        else:
            valor_sin_ceros = []
            encontro_no_cero = False
            for char in valor:
                if char != '0':
                    encontro_no_cero = True
                if encontro_no_cero:
                    valor_sin_ceros.append(char)
            
            return len(valor_sin_ceros) if len(valor_sin_ceros) > 0 else 1

    def _char_a_int(self, char_digit: str) -> int:
        if char_digit >= '0' and char_digit <= '9':
            return ord(char_digit) - ord('0')
        elif char_digit >= 'a' and char_digit <= 'f':
            return ord(char_digit) - ord('a') + 10
        return 0 

    def _int_a_char(self, int_val: int) -> str:
        if 0 <= int_val <= 9:
            return chr(ord('0') + int_val)
        elif 10 <= int_val <= 15:
            return chr(ord('a') + int_val - 10)
        return '0' 

    def _pad_strings_izquierda(self, s1: str, s2: str) -> tuple[str, str]:
        max_len = len(s1) if len(s1) > len(s2) else len(s2)
        s1_padded = ('0' * (max_len - len(s1))) + s1
        s2_padded = ('0' * (max_len - len(s2))) + s2
        return s1_padded, s2_padded

    def _eliminar_ceros_izquierda(self, num_str: str) -> str:
        if len(num_str) == 0:
            return '0'
        inicio = 0
        while inicio < len(num_str) - 1 and num_str[inicio] == '0':
            inicio += 1
        return num_str[inicio:]

    def _sumar_cadenas_manual(self, num1_str: str, num2_str: str, base: int) -> str:
        num1_padded, num2_padded = self._pad_strings_izquierda(num1_str, num2_str)
        result = []
        carry = 0
        for i in range(len(num1_padded) - 1, -1, -1):
            digit1_val = self._char_a_int(num1_padded[i])
            digit2_val = self._char_a_int(num2_padded[i])
            current_sum = digit1_val + digit2_val + carry
            result.append(self._int_a_char(current_sum % base))
            carry = current_sum // base 
        if carry > 0:
            result.append(self._int_a_char(carry))
        return self._eliminar_ceros_izquierda(''.join(reversed(result)))

    def _es_mayor_o_igual(self, num1_str: str, num2_str: str, base: int) -> bool:
        num1_clean = self._eliminar_ceros_izquierda(num1_str)
        num2_clean = self._eliminar_ceros_izquierda(num2_str)
        if len(num1_clean) > len(num2_clean):
            return True
        if len(num1_clean) < len(num2_clean):
            return False
        for i in range(len(num1_clean)):
            digit1 = self._char_a_int(num1_clean[i])
            digit2 = self._char_a_int(num2_clean[i])
            if digit1 > digit2:
                return True
            if digit1 < digit2:
                return False
        return True 

    def _restar_cadenas_manual(self, num1_str: str, num2_str: str, base: int) -> str:
        if not self._es_mayor_o_igual(num1_str, num2_str, base):
            return "ERROR: Resultado negativo"
        num1_padded, num2_padded = self._pad_strings_izquierda(num1_str, num2_str)
        result = []
        borrow = 0
        for i in range(len(num1_padded) - 1, -1, -1):
            digit1_val = self._char_a_int(num1_padded[i])
            digit2_val = self._char_a_int(num2_padded[i])
            current_diff = digit1_val - digit2_val - borrow
            if current_diff < 0:
                current_diff += base
                borrow = 1
            else:
                borrow = 0
            result.append(self._int_a_char(current_diff))
        return self._eliminar_ceros_izquierda(''.join(reversed(result)))

    def _multiplicar_un_digito(self, num_str: str, digit_char: str, base: int) -> str:
        digit_val = self._char_a_int(digit_char)
        result = []
        carry = 0
        for i in range(len(num_str) - 1, -1, -1):
            product = self._char_a_int(num_str[i]) * digit_val + carry 
            result.append(self._int_a_char(product % base))
            carry = product // base
        if carry > 0:
            result.append(self._int_a_char(carry))
        return ''.join(reversed(result))

    def _multiplicar_cadenas_manual(self, num1_str: str, num2_str: str, base: int) -> str:
        partial_products = []
        for i in range(len(num2_str) - 1, -1, -1):
            product_line = self._multiplicar_un_digito(num1_str, num2_str[i], base)
            for _ in range(len(num2_str) - 1 - i):
                product_line += '0'
            partial_products.append(product_line)
        final_sum = '0'
        for p_prod in partial_products:
            final_sum = self._sumar_cadenas_manual(final_sum, p_prod, base)
        return final_sum

    def _dividir_cadenas_manual(self, num1_str: str, num2_str: str, base: int) -> str:
        if num2_str == '0':
            raise ZeroDivisionError("Division por cero")
        num1_str = self._eliminar_ceros_izquierda(num1_str)
        num2_str = self._eliminar_ceros_izquierda(num2_str)
        if num1_str == '0':
            return '0'
        if not self._es_mayor_o_igual(num1_str, num2_str, base):
            return '0'
        cociente = "0"
        dividendo_actual = "" 
        for digit_char in num1_str:
            dividendo_actual += digit_char
            dividendo_actual = self._eliminar_ceros_izquierda(dividendo_actual)
            current_q_digit = 0
            while self._es_mayor_o_igual(dividendo_actual, num2_str, base):
                dividendo_actual = self._restar_cadenas_manual(dividendo_actual, num2_str, base)
                current_q_digit += 1
            cociente += self._int_a_char(current_q_digit)
        return self._eliminar_ceros_izquierda(cociente)

    def _es_numero_valido(self, num_str: str, base: int) -> bool:
        chars_validos = {
            2: '01',
            10: '0123456789',
            16: '0123456789abcdef'
        }.get(base, '')
        for char in num_str:
            if char not in chars_validos:
                return False
        return True

    def _demostrar_operaciones_por_computo(self, valor_str: str, base: int) -> str:
        if '.' in valor_str:
            return "" 
        operando_dec_int = random.randint(1, 9)
        operando_str = ""
        if base == 10:
            operando_str = str(operando_dec_int)
        else:
            temp_val = operando_dec_int
            while temp_val > 0:
                operando_str = self._int_a_char(temp_val % base) + operando_str
                temp_val = temp_val // base
        
        operaciones_posibles = []
        try:
            resultado_suma = self._sumar_cadenas_manual(valor_str, operando_str, base)
            if self._es_numero_valido(resultado_suma, base):
                operaciones_posibles.append('+')
        except:
            pass
        try:
            resultado_resta = self._restar_cadenas_manual(valor_str, operando_str, base)
            if not resultado_resta.startswith("ERROR:") and self._es_numero_valido(resultado_resta, base):
                operaciones_posibles.append('-')
        except:
            pass
        try:
            resultado_mult = self._multiplicar_cadenas_manual(valor_str, operando_str, base)
            if self._es_numero_valido(resultado_mult, base):
                operaciones_posibles.append('*')
        except:
            pass
        try:
            if operando_str != '0':
                resultado_div = self._dividir_cadenas_manual(valor_str, operando_str, base)
                if self._es_numero_valido(resultado_div, base):
                    operaciones_posibles.append('/')
        except:
            pass
        return ''.join(operaciones_posibles)

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

num = Numero("10")
print(num.resultado_completo())
num = Numero("1010")
print(num.resultado_completo())