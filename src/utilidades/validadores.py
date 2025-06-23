from errores.tiposErrores import (
    DivisionByZeroError,
    MathematicalIndeterminacyError,
    InvalidNumberFormatError,
    MatrixDimensionsError
)

def validateDivisionDenominator(denominatorValue: float):
    if denominatorValue == 0:
        raise DivisionByZeroError("Operacion invalida: division por cero")

def validateNumberFormat(inputValue: str, numberSystem: str):
    if numberSystem == 'Binario':
        if not all(char in '01.' for char in inputValue):
            raise InvalidNumberFormatError(f"Valor '{inputValue}' no es binario valido")
    
    elif numberSystem == 'Decimal':
        try:
            # Convertir considerando comas como puntos decimales
            float(inputValue.replace(',', '.'))
        except ValueError:
            raise InvalidNumberFormatError(f"Valor '{inputValue}' no es decimal valido")
    
    elif numberSystem == 'Hexadecimal':
        validChars = '0123456789abcdefABCDEF.'
        if not all(char in validChars for char in inputValue):
            raise InvalidNumberFormatError(f"Valor '{inputValue}' no es hexadecimal valido")
    
    else:
        raise ValueError(f"Sistema numerico no reconocido: {numberSystem}")

def validateMathematicalOperation(operationSymbol: str, operandValues: list):
    if operationSymbol == '/':
        validateDivisionDenominator(operandValues[1])
    
    elif operationSymbol == '√':
        if operandValues[0] < 0:
            raise MathematicalIndeterminacyError("Operacion invalida: raiz cuadrada de numero negativo")
    
    elif operationSymbol == 'ln':
        if operandValues[0] <= 0:
            raise MathematicalIndeterminacyError("Operación invalida: logaritmo natural de numero no positivo")

def validateMatrixDimensionsForOperation(matrixA, matrixB, operationType: str):
    # Validar matrices no vacias
    if matrixA.rows == 0 or matrixA.columns == 0 or matrixB.rows == 0 or matrixB.columns == 0:
        raise MatrixDimensionsError("Operacion invalida: matrices vacias")
    
    if operationType in ['suma', 'resta']:
        if matrixA.rows != matrixB.rows or matrixA.columns != matrixB.columns:
            raise MatrixDimensionsError(
                f"Dimensiones incompatibles para {operationType}: "
                f"{matrixA.rows}x{matrixA.columns} vs {matrixB.rows}x{matrixB.columns}"
            )
    
    elif operationType == 'producto':
        if matrixA.columns != matrixB.rows:
            raise MatrixDimensionsError(
                f"Dimensiones incompatibles para producto: "
                f"{matrixA.rows}x{matrixA.columns} vs {matrixB.rows}x{matrixB.columns}"
            )