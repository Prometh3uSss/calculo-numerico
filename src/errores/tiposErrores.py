class ErrorNumerico(Exception):
    "Clase base para errores numéricos"
    pass

class DivisionPorCeroError(ErrorNumerico):
    "Error cuando se intenta dividir por cero"
    pass

class IndeterminacionMatematicaError(ErrorNumerico):
    "Error para indeterminaciones matemáticas (0/0, ∞/∞, etc.)"
    pass

class OverflowError(ErrorNumerico):
    "Error cuando un cálculo excede el rango representable"
    pass

class UnderflowError(ErrorNumerico):
    "Error cuando un cálculo resulta en un número demasiado pequeño"
    pass

class FormatoNumeroInvalidoError(ErrorNumerico):
    "Error cuando el formato de un número no es válido"
    pass

class DimensionesMatrizError(ErrorNumerico):
    "Error cuando las dimensiones de las matrices son incompatibles"
    pass