from errores.tiposErrores import (
    DivisionByZeroError,
    MathematicalIndeterminacyError,
    InvalidNumberFormatError,  
    MatrixDimensionsError      
)

def validateDivision(denominator):
    "Valida que el denominador no sea cero"
    if denominator == 0:
        raise DivisionByZeroError("Division por cero no permitida")

def validateNumberFormat(value, numberSystem):
    "Valida el formato de un numero segun su sistema"
    if numberSystem == 'Binario':
        if not all(char in '01.' for char in value):
            raise InvalidNumberFormatError(f"Valor '{value}' no es binario valido")
    
    elif numberSystem == 'Decimal':
        try:
            float(value.replace(',', '.'))
        except ValueError:
            raise InvalidNumberFormatError(f"Valor '{value}' no es decimal valido")
    
    elif numberSystem == 'Hexadecimal':
        if not all(char in '0123456789abcdefABCDEF.' for char in value):
            raise InvalidNumberFormatError(f"Valor '{value}' no es hexadecimal valido")
    
    else:
        raise ValueError(f"Sistema numerico no reconocido: {numberSystem}")

def validateOperation(operator, operands):
    "Valida operaciones matematicas para evitar indeterminaciones"
    if operator == '/':
        validateDivision(operands[1])
    
    elif operator == '√':
        if operands[0] < 0:
            raise MathematicalIndeterminacyError("Raiz cuadrada de numero negativo")
    
    elif operator == 'ln':
        if operands[0] <= 0:
            raise MathematicalIndeterminacyError("Logaritmo natural de numero no positivo")

def validateMatrixDimensions(matrix1, matrix2, operation):
    "Valida que las dimensiones de las matrices sean compatibles"
    if operation == 'suma' or operation == 'resta':
        if matrix1.rows != matrix2.rows or matrix1.columns != matrix2.columns:
            raise MatrixDimensionsError(
                f"Dimensiones incompatibles para {operation}: "
                f"{matrix1.rows}x{matrix1.columns} vs {matrix2.rows}x{matrix2.columns}"
            )
    
    elif operation == 'producto':
        if matrix1.columns != matrix2.rows:
            raise MatrixDimensionsError(
                f"Dimensiones incompatibles para producto: "
                f"{matrix1.rows}x{matrix1.columns} vs {matrix2.rows}x{matrix2.columns}"
            )