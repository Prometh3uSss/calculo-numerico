from errores.tiposErrores import (
    DivisionByZeroError,
    MathematicalIndeterminacyError,
    InvalidNumberFormatError,
    MatrixDimensionsError
)

def validateDivisionDenominator(denominatorValue: float):
    """
    Valida que el denominador de una división no sea cero.
    
    Args:
        denominatorValue: Valor del denominador a validar
        
    Raises:
        DivisionByZeroError: Si el denominador es cero
    """
    if denominatorValue == 0:
        raise DivisionByZeroError("Operación inválida: división por cero")

def validateNumberFormat(inputValue: str, numberSystem: str):
    """
    Valida el formato de un número según el sistema numérico especificado.
    
    Args:
        inputValue: Valor a validar
        numberSystem: Sistema numérico ('Binario', 'Decimal', 'Hexadecimal')
        
    Raises:
        InvalidNumberFormatError: Si el formato no coincide con el sistema
    """
    if numberSystem == 'Binario':
        if not all(char in '01.' for char in inputValue):
            raise InvalidNumberFormatError(f"Valor '{inputValue}' no es binario válido")
    
    elif numberSystem == 'Decimal':
        try:
            # Convertir considerando comas como puntos decimales
            float(inputValue.replace(',', '.'))
        except ValueError:
            raise InvalidNumberFormatError(f"Valor '{inputValue}' no es decimal válido")
    
    elif numberSystem == 'Hexadecimal':
        validChars = '0123456789abcdefABCDEF.'
        if not all(char in validChars for char in inputValue):
            raise InvalidNumberFormatError(f"Valor '{inputValue}' no es hexadecimal válido")
    
    else:
        raise ValueError(f"Sistema numérico no reconocido: {numberSystem}")

def validateMathematicalOperation(operationSymbol: str, operandValues: list):
    """
    Valida una operación matemática para evitar indeterminaciones.
    
    Args:
        operationSymbol: Símbolo de la operación (+, -, *, /, √, ln)
        operandValues: Lista de operandos involucrados
        
    Raises:
        MathematicalIndeterminacyError: Si se detecta una operación indeterminada
        DivisionByZeroError: Si se intenta dividir por cero
    """
    if operationSymbol == '/':
        validateDivisionDenominator(operandValues[1])
    
    elif operationSymbol == '√':
        if operandValues[0] < 0:
            raise MathematicalIndeterminacyError("Operación inválida: raíz cuadrada de número negativo")
    
    elif operationSymbol == 'ln':
        if operandValues[0] <= 0:
            raise MathematicalIndeterminacyError("Operación inválida: logaritmo natural de número no positivo")

def validateMatrixDimensionsForOperation(matrixA, matrixB, operationType: str):
    """
    Valida que las dimensiones de dos matrices sean compatibles para la operación.
    
    Args:
        matrixA: Primera matriz (debe tener atributos rows y columns)
        matrixB: Segunda matriz (debe tener atributos rows y columns)
        operationType: Tipo de operación ('suma', 'resta', 'producto')
        
    Raises:
        MatrixDimensionsError: Si las dimensiones son incompatibles
        ValueError: Si las matrices están vacías
    """
    # Validar matrices no vacías
    if matrixA.rows == 0 or matrixA.columns == 0 or matrixB.rows == 0 or matrixB.columns == 0:
        raise MatrixDimensionsError("Operación inválida: matrices vacías")
    
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