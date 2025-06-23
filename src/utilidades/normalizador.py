def normalizeDecimalNumber(inputValue: str) -> str:
    # Validar entrada
    if not inputValue or not isinstance(inputValue, str):
        raise ValueError("Valor de entrada invalido")
    
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
    
    # Combinar todos los digitos significativos
    significantDigits = integerPart + fractionalPart
    significantDigits = significantDigits.lstrip('0') or '0'
    
    # Manejar caso donde no hay digitos significativos
    if significantDigits == '0':
        return "0"
    
    # Determinar exponente
    exponentValue = 0
    mantissaValue = ""
    
    if integerPart != '0':
        exponentValue = len(integerPart) - 1
        mantissaValue = significantDigits[0] + '.' + significantDigits[1:]
    else:
        # Buscar primer digito no cero en decimal
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
    
    # Combinar digitos significativos
    significantDigits = integerPart + fractionalPart
    significantDigits = significantDigits.lstrip('0') or '0'
    
    if significantDigits == '0':
        return "0"
    
    exponentValue = 0
    mantissaValue = ""
    
    if integerPart != '0':
        exponentValue = len(integerPart) - 1
        mantissaValue = significantDigits[0] + '.' + significantDigits[1:]
    else:
        for index, char in enumerate(fractionalPart):
            if char != '0':
                exponentValue = -(index + 1)
                mantissaValue = fractionalPart[index] + '.' + fractionalPart[index+1:]
                break
    
    if '.' in mantissaValue:
        mantissaValue = mantissaValue.rstrip('0').rstrip('.')
    
    return f"{signCharacter}{mantissaValue} × 2^{exponentValue}"


def normalizeHexadecimalNumber(inputValue: str) -> str:
    # Manejar signo y convertir a mayusculas
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
    
    significantDigits = integerPart + fractionalPart
    significantDigits = significantDigits.lstrip('0') or '0'
    
    if significantDigits == '0':
        return "0"
    
    exponentValue = 0
    mantissaValue = ""
    
    if integerPart != '0':
        exponentValue = len(integerPart) - 1
        mantissaValue = significantDigits[0] + '.' + significantDigits[1:]
    else:
        for index, char in enumerate(fractionalPart):
            if char != '0':
                exponentValue = -(index + 1)
                mantissaValue = fractionalPart[index] + '.' + fractionalPart[index+1:]
                break

    if '.' in mantissaValue:
        mantissaValue = mantissaValue.rstrip('0').rstrip('.')
    
    return f"{signCharacter}{mantissaValue} × 16^{exponentValue}"