from errores.tipos_errores import (
    DivisionPorCeroError,
    IndeterminacionMatematicaError
)

def validarDivision(denominador):
    "Valida que el denominador no sea cero"
    if denominador == 0:
        raise DivisionPorCeroError("Division por cero no permitida")

def validarFormatoNumero(valor, sistema):
    "Valida el formato de un numero segun su sistema"
    if sistema == 'Binario':
        if not all(c in '01.' for c in valor):
            raise FormatoNumeroInvalidoError(f"Valor '{valor}' no es binario valido")
    
    elif sistema == 'Decimal':
        try:
            float(valor.replace(',', '.'))
        except ValueError:
            raise FormatoNumeroInvalidoError(f"Valor '{valor}' no es decimal valido")
    
    elif sistema == 'Hexadecimal':
        if not all(c in '0123456789abcdefABCDEF.' for c in valor):
            raise FormatoNumeroInvalidoError(f"Valor '{valor}' no es hexadecimal valido")
    
    else:
        raise ValueError(f"Sistema numerico no reconocido: {sistema}")

def validarOperacion(operador, operandos):
    "Valida operaciones matematicas para evitar indeterminaciones"
    if operador == '/':
        validarDivision(operandos[1])
    
    elif operador == '√':
        if operandos[0] < 0:
            raise IndeterminacionMatematicaError("Raiz cuadrada de numero negativo")
    
    elif operador == 'ln':
        if operandos[0] <= 0:
            raise IndeterminacionMatematicaError("Logaritmo natural de numero no positivo")

def validarDimensionesMatrices(matriz1, matriz2, operacion):
    "Valida que las dimensiones de las matrices sean compatibles"
    if operacion == 'suma' or operacion == 'resta':
        if matriz1.filas != matriz2.filas or matriz1.columnas != matriz2.columnas:
            raise DimensionesMatrizError(
                f"Dimensiones incompatibles para {operacion}: "
                f"{matriz1.filas}x{matriz1.columnas} vs {matriz2.filas}x{matriz2.columnas}"
            )
    
    elif operacion == 'producto':
        if matriz1.columnas != matriz2.filas:
            raise DimensionesMatrizError(
                f"Dimensiones incompatibles para producto: "
                f"{matriz1.filas}x{matriz1.columnas} vs {matriz2.filas}x{matriz2.columnas}"
            )