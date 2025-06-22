def normalizeDecimal(valueStr: str) -> str:
    """
    Normaliza un número decimal a notación científica
    Ejemplos:
      "123.45" -> "1.2345 × 10^2"
      "0.00123" -> "1.23 × 10^{-3}"
      "1000" -> "1 × 10^3"
    """
    # Manejar signo
    sign = ''
    if valueStr.startswith('-'):
        sign = '-'
        valueStr = valueStr[1:]
    elif valueStr.startswith('+'):
        valueStr = valueStr[1:]
    
    # Reemplazar comas por puntos y eliminar espacios
    valueStr = valueStr.replace(',', '.').replace(' ', '')
    
    # Caso especial: cero
    if all(char in '0.,' for char in valueStr):
        return "0"
    
    # Dividir en parte entera y decimal
    parts = valueStr.split('.')
    integerPart = parts[0].lstrip('0') or '0'
    
    if len(parts) > 1:
        fractionalPart = parts[1]
    else:
        fractionalPart = ""
    
    # Combinar todos los dígitos significativos
    significantDigits = integerPart + fractionalPart
    significantDigits = significantDigits.lstrip('0') or '0'
    
    # Manejar caso donde no hay dígitos significativos
    if significantDigits == '0':
        return "0"
    
    # Determinar exponente
    if integerPart != '0':
        exponent = len(integerPart) - 1
        mantissa = significantDigits[0] + '.' + significantDigits[1:]
    else:
        # Buscar primer dígito no cero en decimal
        for index, char in enumerate(fractionalPart):
            if char != '0':
                exponent = -(index + 1)
                mantissa = fractionalPart[index] + '.' + fractionalPart[index+1:]
                break
    
    # Limpiar mantisa (quitar ceros finales)
    if '.' in mantissa:
        mantissa = mantissa.rstrip('0').rstrip('.')
    
    return f"{sign}{mantissa} × 10^{exponent}"


def normalizeBinary(valueStr: str) -> str:
    """
    Normaliza un número binario a notación científica
    Ejemplos:
      "101.01" -> "1.0101 × 2^2"
      "0.00101" -> "1.01 × 2^{-3}"
    """
    # Manejar signo (binarios normalmente sin signo)
    sign = ''
    if valueStr.startswith('-'):
        sign = '-'
        valueStr = valueStr[1:]
    elif valueStr.startswith('+'):
        valueStr = valueStr[1:]
    
    # Reemplazar comas por puntos
    valueStr = valueStr.replace(',', '.')
    
    # Caso especial: cero
    if all(char in '0.,' for char in valueStr):
        return "0"
    
    # Dividir en parte entera y decimal
    parts = valueStr.split('.')
    integerPart = parts[0].lstrip('0') or '0'
    
    if len(parts) > 1:
        fractionalPart = parts[1]
    else:
        fractionalPart = ""
    
    # Combinar dígitos significativos
    significantDigits = integerPart + fractionalPart
    significantDigits = significantDigits.lstrip('0') or '0'
    
    if significantDigits == '0':
        return "0"
    
    # Determinar exponente
    if integerPart != '0':
        exponent = len(integerPart) - 1
        mantissa = significantDigits[0] + '.' + significantDigits[1:]
    else:
        for index, char in enumerate(fractionalPart):
            if char != '0':
                exponent = -(index + 1)
                mantissa = fractionalPart[index] + '.' + fractionalPart[index+1:]
                break
    
    # Limpiar mantisa
    if '.' in mantissa:
        mantissa = mantissa.rstrip('0').rstrip('.')
    
    return f"{sign}{mantissa} × 2^{exponent}"


def normalizeHexadecimal(valueStr: str) -> str:
    """
    Normaliza un número hexadecimal a notación científica
    Ejemplos:
      "1A.3F" -> "1.A3F × 16^1"
      "0.00F2" -> "F.2 × 16^{-3}"
    """
    # Manejar signo y convertir a mayúsculas
    sign = ''
    if valueStr.startswith('-'):
        sign = '-'
        valueStr = valueStr[1:]
    elif valueStr.startswith('+'):
        valueStr = valueStr[1:]
    
    valueStr = valueStr.upper().replace(',', '.')
    
    # Caso especial: cero
    if all(char in '0.,' for char in valueStr):
        return "0"
    
    # Dividir en parte entera y decimal
    parts = valueStr.split('.')
    integerPart = parts[0].lstrip('0') or '0'
    
    if len(parts) > 1:
        fractionalPart = parts[1]
    else:
        fractionalPart = ""
    
    # Combinar dígitos significativos
    significantDigits = integerPart + fractionalPart
    significantDigits = significantDigits.lstrip('0') or '0'
    
    if significantDigits == '0':
        return "0"
    
    # Determinar exponente
    if integerPart != '0':
        exponent = len(integerPart) - 1
        mantissa = significantDigits[0] + '.' + significantDigits[1:]
    else:
        for index, char in enumerate(fractionalPart):
            if char != '0':
                exponent = -(index + 1)
                mantissa = fractionalPart[index] + '.' + fractionalPart[index+1:]
                break
    
    # Limpiar mantisa
    if '.' in mantissa:
        mantissa = mantissa.rstrip('0').rstrip('.')
    
    return f"{sign}{mantissa} × 16^{exponent}"