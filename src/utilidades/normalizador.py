from core.tiposUtilidades import allElementsMeet

def normalizeDecimalNumber(inputValue: str) -> str:

    if not inputValue or not isinstance(inputValue, str):
        raise ValueError("Valor de entrada no valido")
    
    signCharacter = ''
    if inputValue.startswith('-'):
        signCharacter = '-'
        processedValue = inputValue[1:]
    elif inputValue.startswith('+'):
        processedValue = inputValue[1:]
    else:
        processedValue = inputValue

    processedValue = processedValue.replace(',', '.').replace(' ', '')
    
    if allElementsMeet(processedValue, lambda char: char in '0.,'):
        return "0"
    
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
    
    return f"{signCharacter}{mantissaValue} × 10^{exponentValue}"


def normalizeBinaryNumber(inputValue: str) -> str:
    signCharacter = ''
    if inputValue.startswith('-'):
        signCharacter = '-'
        processedValue = inputValue[1:]
    elif inputValue.startswith('+'):
        processedValue = inputValue[1:]
    else:
        processedValue = inputValue
    
    processedValue = processedValue.replace(',', '.')
    
    if allElementsMeet(processedValue, lambda char: char in '0.,'):
        return "0"
    
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
    signCharacter = ''
    if inputValue.startswith('-'):
        signCharacter = '-'
        processedValue = inputValue[1:]
    elif inputValue.startswith('+'):
        processedValue = inputValue[1:]
    else:
        processedValue = inputValue
    
    processedValue = processedValue.upper().replace(',', '.')
    
    if allElementsMeet(processedValue, lambda char: char in '0.,'):
        return "0"
    
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