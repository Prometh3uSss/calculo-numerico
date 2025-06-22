def normalizar_decimal(valor: str) -> str:
    """
    Normaliza un número decimal a notación científica
    Ejemplos:
      "123.45" -> "1.2345 × 10^2"
      "0.00123" -> "1.23 × 10^{-3}"
      "1000" -> "1 × 10^3"
    """
    # Manejar signo
    signo = ''
    if valor.startswith('-'):
        signo = '-'
        valor = valor[1:]
    elif valor.startswith('+'):
        valor = valor[1:]
    
    # Reemplazar comas por puntos y eliminar espacios
    valor = valor.replace(',', '.').replace(' ', '')
    
    # Caso especial: cero
    if all(c in '0.,' for c in valor):
        return "0"
    
    # Dividir en parte entera y decimal
    partes = valor.split('.')
    parte_entera = partes[0].lstrip('0') or '0'
    
    if len(partes) > 1:
        parte_decimal = partes[1]
    else:
        parte_decimal = ""
    
    # Combinar todos los dígitos significativos
    digitos = parte_entera + parte_decimal
    digitos = digitos.lstrip('0') or '0'
    
    # Manejar caso donde no hay dígitos significativos
    if digitos == '0':
        return "0"
    
    # Determinar exponente
    if parte_entera != '0':
        exponente = len(parte_entera) - 1
        mantisa = digitos[0] + '.' + digitos[1:]
    else:
        # Buscar primer dígito no cero en decimal
        for i, char in enumerate(parte_decimal):
            if char != '0':
                exponente = -(i + 1)
                mantisa = parte_decimal[i] + '.' + parte_decimal[i+1:]
                break
    
    # Limpiar mantisa (quitar ceros finales)
    if '.' in mantisa:
        mantisa = mantisa.rstrip('0').rstrip('.')
    
    return f"{signo}{mantisa} × 10^{exponente}"


def normalizar_binario(valor: str) -> str:
    """
    Normaliza un número binario a notación científica
    Ejemplos:
      "101.01" -> "1.0101 × 2^2"
      "0.00101" -> "1.01 × 2^{-3}"
    """
    # Manejar signo (binarios normalmente sin signo)
    signo = ''
    if valor.startswith('-'):
        signo = '-'
        valor = valor[1:]
    elif valor.startswith('+'):
        valor = valor[1:]
    
    # Reemplazar comas por puntos
    valor = valor.replace(',', '.')
    
    # Caso especial: cero
    if all(c in '0.,' for c in valor):
        return "0"
    
    # Dividir en parte entera y decimal
    partes = valor.split('.')
    parte_entera = partes[0].lstrip('0') or '0'
    
    if len(partes) > 1:
        parte_decimal = partes[1]
    else:
        parte_decimal = ""
    
    # Combinar dígitos significativos
    digitos = parte_entera + parte_decimal
    digitos = digitos.lstrip('0') or '0'
    
    if digitos == '0':
        return "0"
    
    # Determinar exponente
    if parte_entera != '0':
        exponente = len(parte_entera) - 1
        mantisa = digitos[0] + '.' + digitos[1:]
    else:
        for i, char in enumerate(parte_decimal):
            if char != '0':
                exponente = -(i + 1)
                mantisa = parte_decimal[i] + '.' + parte_decimal[i+1:]
                break
    
    # Limpiar mantisa
    if '.' in mantisa:
        mantisa = mantisa.rstrip('0').rstrip('.')
    
    return f"{signo}{mantisa} × 2^{exponente}"


def normalizar_hexadecimal(valor: str) -> str:
    """
    Normaliza un número hexadecimal a notación científica
    Ejemplos:
      "1A.3F" -> "1.A3F × 16^1"
      "0.00F2" -> "F.2 × 16^{-3}"
    """
    # Manejar signo y convertir a mayúsculas
    signo = ''
    if valor.startswith('-'):
        signo = '-'
        valor = valor[1:]
    elif valor.startswith('+'):
        valor = valor[1:]
    
    valor = valor.upper().replace(',', '.')
    
    # Caso especial: cero
    if all(c in '0.,' for c in valor):
        return "0"
    
    # Dividir en parte entera y decimal
    partes = valor.split('.')
    parte_entera = partes[0].lstrip('0') or '0'
    
    if len(partes) > 1:
        parte_decimal = partes[1]
    else:
        parte_decimal = ""
    
    # Combinar dígitos significativos
    digitos = parte_entera + parte_decimal
    digitos = digitos.lstrip('0') or '0'
    
    if digitos == '0':
        return "0"
    
    # Determinar exponente
    if parte_entera != '0':
        exponente = len(parte_entera) - 1
        mantisa = digitos[0] + '.' + digitos[1:]
    else:
        for i, char in enumerate(parte_decimal):
            if char != '0':
                exponente = -(i + 1)
                mantisa = parte_decimal[i] + '.' + parte_decimal[i+1:]
                break
    
    # Limpiar mantisa
    if '.' in mantisa:
        mantisa = mantisa.rstrip('0').rstrip('.')
    
    return f"{signo}{mantisa} × 16^{exponente}"
