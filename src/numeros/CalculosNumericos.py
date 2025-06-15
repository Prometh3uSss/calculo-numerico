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
            
            ops_demostrables_simbolos = self._demostrar_operaciones_por_computo(valor, base)
            operaciones.append(ops_demostrables_simbolos)
        
        self.formas_normalizadas = np.array(formas, dtype=object)
        self.cifras_significativas = np.array(cifras, dtype=int)
        self.operaciones_posibles = np.array(operaciones, dtype=object)
    
    def _es_binario(self, valor: str) -> bool:
        tiene_punto = False
        for char in valor:
            if char == '.':
                if tiene_punto: return False 
                tiene_punto = True
            elif char not in '01':
                return False
        return True
    
    def _es_decimal(self, valor: str) -> bool:
        tiene_punto = False
        for char in valor:
            if char == '.':
                if tiene_punto: return False 
                tiene_punto = True
            elif char not in '0123456789':
                return False
        return True
    
    def _es_hexadecimal(self, valor: str) -> bool:
        tiene_punto = False
        for char in valor:
            if char == '.':
                if tiene_punto: return False 
                tiene_punto = True
            elif char not in '0123456789abcdef':
                return False
        return True
    
    def _calcular_forma_normalizada(self, valor: str, base: int) -> str:
        punto_indice = -1
        for i in range(len(valor)):
            if valor[i] == '.':
                punto_indice = i
                break
        
        if punto_indice != -1:
            entera = valor[0:punto_indice]
            decimal = valor[punto_indice+1:]
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
            inicio_dec = 0
            while inicio_dec < len(decimal) and decimal[inicio_dec] == '0':
                inicio_dec += 1
            if inicio_dec < len(decimal):
                mantisa = decimal[inicio_dec]
                for i in range(inicio_dec + 1, len(decimal)):
                    mantisa += decimal[i]
                exponente = -inicio_dec - 1
            else:
                return "0"
        else:
            return "0"
        
        return f"{mantisa} x {base}^{exponente}"
    
    def _contar_cifras_significativas(self, valor: str, base: int) -> int:
        es_negativo = False
        if len(valor) > 0 and valor[0] == '-':
            es_negativo = True
            valor_procesado = ""
            for i in range(1, len(valor)):
                valor_procesado += valor[i]
        else:
            valor_procesado = valor

        valor_sin_punto = ""
        tiene_punto = False
        for char in valor_procesado:
            if char == '.':
                tiene_punto = True
            else:
                valor_sin_punto += char
            
        inicio_significativo = 0
        while inicio_significativo < len(valor_sin_punto) and valor_sin_punto[inicio_significativo] == '0':
            inicio_significativo += 1
        
        if inicio_significativo == len(valor_sin_punto):
            return 1 

        if tiene_punto: 
            return len(valor_sin_punto) - inicio_significativo
        else: 
            valor_sin_ceros_izquierda = ""
            encontro_digito_no_cero = False
            for char in valor_procesado:
                if char != '0':
                    encontro_digito_no_cero = True
                if encontro_digito_no_cero:
                    valor_sin_ceros_izquierda += char
            
            if not valor_sin_ceros_izquierda:
                return 1 
            
            return len(valor_sin_ceros_izquierda)

    def _char_a_int(self, char_digit: str) -> int:
        """Convierte un caracter digito (0-9, a-f) a su valor entero."""
        if '0' <= char_digit <= '9':
            return ord(char_digit) - ord('0')
        elif 'a' <= char_digit <= 'f':
            return ord(char_digit) - ord('a') + 10
        return 0 

    def _int_a_char(self, int_val: int) -> str:
        """Convierte un valor entero (0-15) a su caracter digito (0-9, A-F)."""
        if 0 <= int_val <= 9:
            return chr(ord('0') + int_val)
        elif 10 <= int_val <= 15:
            return chr(ord('a') + int_val - 10)
        return '0' 

    def _pad_strings_izquierda(self, s1: str, s2: str, pad_char='0') -> tuple[str, str]:
        """Rellena con un caracter a la izquierda para igualar longitudes."""
        max_len = len(s1) if len(s1) > len(s2) else len(s2)
        padded_s1 = pad_char * (max_len - len(s1)) + s1
        padded_s2 = pad_char * (max_len - len(s2)) + s2
        return padded_s1, padded_s2

    def _eliminar_ceros_izquierda(self, num_str: str) -> str:
        """Elimina ceros a la izquierda de una cadena numerica."""
        if len(num_str) == 0:
            return '0'
        idx = 0
        while idx < len(num_str) - 1 and num_str[idx] == '0':
            idx += 1
        return num_str[idx:]

    def _sumar_cadenas_manual(self, num1_str: str, num2_str: str, base: int) -> str:
        """Suma dos numeros representados como cadenas en una base dada."""
        num1_padded, num2_padded = self._pad_strings_izquierda(num1_str, num2_str)
        
        result = []
        carry = 0
        
        for i in range(len(num1_padded) - 1, -1, -1):
            digit1_val = self._char_a_int(num1_padded[i])
            digit2_val = self._char_a_int(num2_padded[i])
            
            current_sum = digit1_val + digit2_val + carry
            digit_result = current_sum % base
            carry = current_sum // base 
            
            result.append(self._int_a_char(digit_result))
            
        if carry > 0:
            result.append(self._int_a_char(carry))
            
        final_result = "".join(reversed(result))
        return self._eliminar_ceros_izquierda(final_result)

    def _es_mayor_o_igual(self, num1_str: str, num2_str: str, base: int) -> bool:
        """Compara si num1_str es mayor o igual que num2_str en una base dada."""
        num1_cleaned = self._eliminar_ceros_izquierda(num1_str)
        num2_cleaned = self._eliminar_ceros_izquierda(num2_str)

        len1 = len(num1_cleaned)
        len2 = len(num2_cleaned)

        if len1 > len2:
            return True
        if len1 < len2:
            return False

        for i in range(len1):
            digit1 = self._char_a_int(num1_cleaned[i])
            digit2 = self._char_a_int(num2_cleaned[i])
            if digit1 > digit2:
                return True
            if digit1 < digit2:
                return False
        
        return True 

    def _restar_cadenas_manual(self, num1_str: str, num2_str: str, base: int) -> str:
        """Resta dos numeros representados como cadenas en una base dada (num1 - num2).
           Asume num1 >= num2. No maneja negativos.
        """
        if not self._es_mayor_o_igual(num1_str, num2_str, base):
            return "ERROR: Resultado negativo (no soportado)"
        
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
            
        final_result = "".join(reversed(result))
        return self._eliminar_ceros_izquierda(final_result)

    def _multiplicar_un_digito(self, num_str: str, digit_char: str, base: int) -> str:
        """Multiplica una cadena numerica por un solo digito en la misma base."""
        if digit_char == '0':
            return '0'
        
        digit_val = self._char_a_int(digit_char)
        
        result = []
        carry = 0
        
        for i in range(len(num_str) - 1, -1, -1):
            num_digit_val = self._char_a_int(num_str[i])
            product = num_digit_val * digit_val + carry 
            
            result_digit = product % base
            carry = product // base
            
            result.append(self._int_a_char(result_digit))
            
        if carry > 0:
            result.append(self._int_a_char(carry))
            
        return "".join(reversed(result))

    def _multiplicar_cadenas_manual(self, num1_str: str, num2_str: str, base: int) -> str:
        """Multiplica dos numeros representados como cadenas en una base dada."""
        if num1_str == '0' or num2_str == '0':
            return '0'
        
        num1_str = self._eliminar_ceros_izquierda(num1_str)
        num2_str = self._eliminar_ceros_izquierda(num2_str)

        partial_products = []
        
        for i in range(len(num2_str) - 1, -1, -1):
            digit2_char = num2_str[i]
            product_line = self._multiplicar_un_digito(num1_str, digit2_char, base)
            
            for _ in range(len(num2_str) - 1 - i):
                product_line += '0'
            
            partial_products.append(product_line)
        
        final_sum = '0'
        for p_prod in partial_products:
            final_sum = self._sumar_cadenas_manual(final_sum, p_prod, base)
            
        return self._eliminar_ceros_izquierda(final_sum)

    def _dividir_cadenas_manual(self, num1_str: str, num2_str: str, base: int) -> str:
        """Divide dos numeros representados como cadenas en una base dada (num1 / num2).
           Devuelve solo la parte entera del cociente.
           Requiere implementacion de resta y comparacion de cadenas.
        """
        if num2_str == '0':
            raise ZeroDivisionError("Division por cero no es posible.")

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
                temp_inc = self._sumar_cadenas_manual(self._int_a_char(current_q_digit), '1', base)
                current_q_digit = self._char_a_int(temp_inc) 
                if len(temp_inc) > 1: 
                    pass 

            cociente += self._int_a_char(current_q_digit)
            
        return self._eliminar_ceros_izquierda(cociente)

    def _demostrar_operaciones_por_computo(self, valor_str: str, base: int) -> str:
        operaciones_posibles = []
        
        operando_dec_int = random.randint(1, 9)

        operando_str = ""
        temp_val = operando_dec_int
        if base == 10:
            operando_str = str(operando_dec_int) 
        else: 
            if temp_val == 0:
                operando_str = '0'
            else:
                while temp_val > 0:
                    remainder = temp_val % base
                    operando_str = self._int_a_char(remainder) + operando_str
                    temp_val = temp_val // base 
        
        if '.' in valor_str:
            return "" 
        
        try:
            self._sumar_cadenas_manual(valor_str, operando_str, base)
            operaciones_posibles.append('+')
        except Exception:
            pass

        try:
            if self._es_mayor_o_igual(valor_str, operando_str, base):
                self._restar_cadenas_manual(valor_str, operando_str, base)
                operaciones_posibles.append('-')
        except Exception:
            pass
        
        try:
            self._multiplicar_cadenas_manual(valor_str, operando_str, base)
            operaciones_posibles.append('*')
        except Exception:
            pass
        
        try:
            if operando_str != '0': 
                self._dividir_cadenas_manual(valor_str, operando_str, base)
                operaciones_posibles.append('/')
            else:
                pass 
        except ZeroDivisionError:
            pass
        except Exception:
            pass
        
        return "".join(operaciones_posibles)

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