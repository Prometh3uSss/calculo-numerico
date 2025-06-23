def normalizeDecimalNumber(inputValue: str) -> str:
    """
    Normaliza un número decimal a notación científica.
    Ejemplos:
    "123.45" -> "1.2345 × 10^2"
    "-0.00123" -> "-1.23 × 10^{-3}"
    "+1000" -> "1 × 10^3"
    
    Args:
        inputValue: Cadena con número decimal
        
    Returns:
        Representación en notación científica
        
    Raises:
        ValueError: Si el formato es inválido
    """
    # Validar entrada
    if not inputValue or not isinstance(inputValue, str):
        raise ValueError("Valor de entrada inválido")
    
    # Manejar signo
    signCharacter = ''
    if inputValue.startswith('-'):
        signCharacter = '-'
        processedValue = inputValue[1:]
    elif inputValue.startswith('+'):
        processedValue = inputValue[1:]
    else:
        processedValue = inputValue
    
    # Normalizar formato (comas a puntos, eliminar espacios)
    processedValue = processedValue.replace(',', '.').replace(' ', '')
    
    # Caso especial: cero
    if all(char in '0.,' for char in processedValue):
        return "0"
    
    # Dividir en parte entera y decimal
    parts = processedValue.split('.')
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
        exponentValue = len(integerPart) - 1
        mantissaValue = significantDigits[0] + '.' + significantDigits[1:]
    else:
        # Buscar primer dígito no cero en decimal
        for index, char in enumerate(fractionalPart):
            if char != '0':
                exponentValue = -(index + 1)
                mantissaValue = fractionalPart[index] + '.' + fractionalPart[index+1:]
                break
    
    # Limpiar mantisa (quitar ceros finales)
    if '.' in mantissaValue:
        mantissaValue = mantissaValue.rstrip('0').rstrip('.')
    
    return f"{signCharacter}{mantissaValue} × 10^{exponentValue}"


def normalizeBinaryNumber(inputValue: str) -> str:
    """
    Normaliza un número binario a notación científica.
    Ejemplos:
    "101.01" -> "1.0101 × 2^2"
    "-0.00101" -> "-1.01 × 2^{-3}"
    
    Args:
        inputValue: Cadena con número binario
        
    Returns:
        Representación en notación científica binaria
    """
    # Manejar signo
    signCharacter = ''
    if inputValue.startswith('-'):
        signCharacter = '-'
        processedValue = inputValue[1:]
    elif inputValue.startswith('+'):
        processedValue = inputValue[1:]
    else:
        processedValue = inputValue
    
    processedValue = processedValue.replace(',', '.')
    
    # Caso especial: cero
    if all(char in '0.,' for char in processedValue):
        return "0"
    
    # Dividir en parte entera y decimal
    parts = processedValue.split('.')
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
        exponentValue = len(integerPart) - 1
        mantissaValue = significantDigits[0] + '.' + significantDigits[1:]
    else:
        for index, char in enumerate(fractionalPart):
            if char != '0':
                exponentValue = -(index + 1)
                mantissaValue = fractionalPart[index] + '.' + fractionalPart[index+1:]
                break
    
    # Limpiar mantisa
    if '.' in mantissaValue:
        mantissaValue = mantissaValue.rstrip('0').rstrip('.')
    
    return f"{signCharacter}{mantissaValue} × 2^{exponentValue}"


def normalizeHexadecimalNumber(inputValue: str) -> str:
    """
    Normaliza un número hexadecimal a notación científica.
    Ejemplos:
    "1A.3F" -> "1.A3F × 16^1"
    "-0.00F2" -> "-F.2 × 16^{-3}"
    
    Args:
        inputValue: Cadena con número hexadecimal
        
    Returns:
        Representación en notación científica hexadecimal
    """
    # Manejar signo y convertir a mayúsculas
    signCharacter = ''
    if inputValue.startswith('-'):
        signCharacter = '-'
        processedValue = inputValue[1:]
    elif inputValue.startswith('+'):
        processedValue = inputValue[1:]
    else:
        processedValue = inputValue
    
    processedValue = processedValue.upper().replace(',', '.')
    
    # Caso especial: cero
    if all(char in '0.,' for char in processedValue):
        return "0"
    
    # Dividir en parte entera y decimal
    parts = processedValue.split('.')
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
        exponentValue = len(integerPart) - 1
        mantissaValue = significantDigits[0] + '.' + significantDigits[1:]
    else:
        for index, char in enumerate(fractionalPart):
            if char != '0':
                exponentValue = -(index + 1)
                mantissaValue = fractionalPart[index] + '.' + fractionalPart[index+1:]
                break
    
    # Limpiar mantisa
    if '.' in mantissaValue:
        mantissaValue = mantissaValue.rstrip('0').rstrip('.')
    
    return f"{signCharacter}{mantissaValue} × 16^{exponentValue}"