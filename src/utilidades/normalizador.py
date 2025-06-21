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
        return normalizarDecimal(valor)
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

def normalizarDecimal(valor):
    valor = valor.replace(',', '.')
    try:
        num = float(valor)
    except ValueError:
        raise FormatoNumeroInvalidoError(f"Valor '{valor}' no es decimal valido")
    
    if num == 0:
        return '0', 0
    
    exponente = 0
    abs_num = abs(num)
    
    if abs_num >= 1:
        while abs_num >= 10:
            abs_num /= 10
            exponente += 1
    else:
        while abs_num < 1:
            abs_num *= 10
            exponente -= 1
    
    return f"{abs_num:.5f}".rstrip('0').rstrip('.'), exponente

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