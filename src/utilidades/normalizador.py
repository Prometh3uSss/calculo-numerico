def normalizarNumero(valor, sistema):
    """
    Normaliza un numero a su forma cientifica segun su sistema numerico
    :param valor: Valor numerico en formato string
    :param sistema: Sistema numerico ('Binario', 'Decimal', 'Hexadecimal')
    :return: Tupla (mantisa, exponente)
    """
    if sistema == 'Binario':
        return normalizarBinario(valor)
    elif sistema == 'Decimal':
        return normalizar_decimal(valor)
    elif sistema == 'Hexadecimal':
        return normalizarHexadecimal(valor)
    else:
        raise ValueError(f"Sistema numerico no soportado: {sistema}")

def normalizarBinario(valor):
    partes = valor.split('.')
    entero = partes[0].lstrip('0') or '0'
    
    if len(partes) > 1:
        decimal = partes[1].rstrip('0')
    else:
        decimal = ''
    
    
    if entero == '0' and decimal == '':
        return '0', 0
    
    
    if entero != '0':
        exponente = len(entero) - 1
        mantisa = entero[0] + '.' + entero[1:] + decimal
        mantisa = mantisa.rstrip('.').rstrip('0')
        if mantisa.endswith('.'):
            mantisa = mantisa[:-1]
        return mantisa, exponente
    else:
        
        pos = decimal.find('1')
        if pos == -1:  
            return '0', 0
        exponente = -(pos + 1)
        mantisa = '1.' + decimal[pos+1:]
        mantisa = mantisa.rstrip('0').rstrip('.')
        return mantisa, exponente

def normalizar_decimal(valor: str) -> str:
    """Convierte un número decimal a notación científica"""
    # Manejar signo
    signo = ''
    if valor.startswith('-'):
        signo = '-'
        valor = valor[1:]
    elif valor.startswith('+'):
        valor = valor[1:]
    
    # Caso especial: cero
    if all(c in '0.,' for c in valor):
        return "0"
    
    # Dividir en parte entera y decimal
    partes = valor.replace(',', '.').split('.')
    parte_entera = partes[0].lstrip('0') or '0'
    
    if len(partes) > 1:
        parte_decimal = partes[1]
    else:
        parte_decimal = ""
    
    # Combinar todos los dígitos
    digitos = parte_entera + parte_decimal
    digitos = digitos.lstrip('0')
    
    # Encontrar el primer dígito significativo
    if not digitos:
        return "0"
    
    exponente = 0
    
    if parte_entera != '0':
        # Caso con dígitos en parte entera
        exponente = len(parte_entera) - 1
        mantisa = digitos[0] + '.' + digitos[1:]
    else:
        # Caso con ceros en parte entera
        for i, d in enumerate(parte_decimal):
            if d != '0':
                exponente = -(i + 1)
                mantisa = d + '.' + parte_decimal[i+1:]
                break
        else:
            mantisa = '0'
    
    # Eliminar ceros no significativos
    if '.' in mantisa:
        mantisa = mantisa.rstrip('0').rstrip('.')
    
    return f"{signo}{mantisa} × 10^{exponente}"

def normalizarHexadecimal(valor):
    partes = valor.split('.')
    entero = partes[0].lstrip('0') or '0'
    
    if len(partes) > 1:
        decimal = partes[1].rstrip('0')
    else:
        decimal = ''
    
    
    if entero == '0' and decimal == '':
        return '0', 0
    
    
    if entero != '0':
        exponente = len(entero) - 1
        mantisa = entero[0] + '.' + entero[1:] + decimal
        mantisa = mantisa.rstrip('.').rstrip('0')
        if mantisa.endswith('.'):
            mantisa = mantisa[:-1]
        return mantisa, exponente
    else:
        
        for i, char in enumerate(decimal):
            if char != '0':
                exponente = -(i + 1)
                mantisa = char + '.' + decimal[i+1:]
                mantisa = mantisa.rstrip('0').rstrip('.')
                return mantisa, exponente
        return '0', 0