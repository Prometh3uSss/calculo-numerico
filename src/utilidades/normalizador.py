from estructuras.listaEnlazada import LinkedList
from core.tiposUtilidades import allElementsMeet

class StringUtils:
    @staticmethod
    def custom_split(input_str: str, separator: str) -> LinkedList:
        parts = LinkedList()
        current_part = ""
        for char in input_str:
            if char == separator:
                parts.addElementAtEnd(current_part)
                current_part = ""
            else:
                current_part += char
        parts.addElementAtEnd(current_part)
        return parts

    @staticmethod
    def custom_lstrip(input_str: str, chars: str) -> str:
        start = 0
        while start < len(input_str) and input_str[start] in chars:
            start += 1
        return input_str[start:]

    @staticmethod
    def custom_rstrip(input_str: str, chars: str) -> str:
        end = len(input_str) - 1
        while end >= 0 and input_str[end] in chars:
            end -= 1
        return input_str[:end + 1]

    @staticmethod
    def count_leading_zeros(s: str) -> int:
        count = 0
        for char in s:
            if char == '0':
                count += 1
            else:
                break
        return count

def normalizeNumber(inputValue: str, base: int) -> str:
    sign = '-' if inputValue.startswith('-') else ''
    processedValue = inputValue.lstrip('-+').upper().replace(',', '.').replace(' ', '')
    
    if allElementsMeet(processedValue, lambda c: c in '0.'):
        return "0"

    parts = StringUtils.custom_split(processedValue, '.')
    integerPart = parts.getElementAtIndex(0) if parts.getListLength() > 0 else "0"
    fractionalPart = parts.getElementAtIndex(1) if parts.getListLength() > 1 else ""

    integerPart = StringUtils.custom_lstrip(integerPart, '0') or '0'
    fractionalPart = StringUtils.custom_rstrip(fractionalPart, '0')
    
    sigDigits = integerPart + fractionalPart
    sigDigits = StringUtils.custom_lstrip(sigDigits, '0') or '0'

    if sigDigits == '0':
        return "0"

    if integerPart != '0':
        exponent = len(integerPart) - 1
        mantissa = sigDigits[0] + '.' + sigDigits[1:]
    else:
        leadingZeros = StringUtils.count_leading_zeros(fractionalPart)
        exponent = -(leadingZeros + 1)
        mantissa = fractionalPart[leadingZeros] + '.' + fractionalPart[leadingZeros + 1:]

    mantissa = StringUtils.custom_rstrip(mantissa, '0')
    mantissa = StringUtils.custom_rstrip(mantissa, '.')
    
    return f"{sign}{mantissa} × {base}^{exponent}"

def normalizeDecimalNumber(inputValue: str) -> str:
    return normalizeNumber(inputValue, 10)

def normalizeBinaryNumber(inputValue: str) -> str:
    return normalizeNumber(inputValue, 2)

def normalizeHexadecimalNumber(inputValue: str) -> str:
    return normalizeNumber(inputValue, 16)