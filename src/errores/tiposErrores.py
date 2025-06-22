class NumericError(Exception):
    "Clase base para errores numéricos"
    pass

class DivisionByZeroError(NumericError):
    "Error cuando se intenta dividir por cero"
    pass

class MathematicalIndeterminacyError(NumericError):
    "Error para indeterminaciones matemáticas (0/0, ∞/∞, etc.)"
    pass

class NumericOverflowError(NumericError):
    "Error cuando un cálculo excede el rango representable"
    pass

class NumericUnderflowError(NumericError):
    "Error cuando un cálculo resulta en un número demasiado pequeño"
    pass

class InvalidNumberFormatError(NumericError):
    "Error cuando el formato de un número no es válido"
    pass

class MatrixDimensionsError(NumericError):
    "Error cuando las dimensiones de las matrices son incompatibles"
    pass