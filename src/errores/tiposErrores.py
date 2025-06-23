class ProjectBaseException(Exception):
    """Excepcion base para todos los errores personalizados del proyecto"""
    pass

class NumericCalculationException(ProjectBaseException):
    """Clase base para errores relacionados con calculos numericos"""
    pass

class FileOperationException(ProjectBaseException):
    """Clase base para errores relacionados con operaciones de archivos"""
    pass

# ===== Numeric Errors =====
class DivisionByZeroError(NumericCalculationException):
    """Se intento realizar una división donde el denominador es cero"""
    pass

class MathematicalIndeterminacyError(NumericCalculationException):
    """Operacion matematica con resultado indeterminado (0/0, ∞/∞, etc.)"""
    pass

class NumericOverflowError(NumericCalculationException):
    """El resultado de un calculo excede el rango numerico representable"""
    pass

class NumericUnderflowError(NumericCalculationException):
    """El resultado de un calculo es un numero demasiado pequeño para ser representado"""
    pass

class InvalidNumberFormatError(NumericCalculationException):
    """El formato de un numero no coincide con el sistema numerico esperado"""
    pass

class MatrixDimensionsError(NumericCalculationException):
    """Las dimensiones de las matrices son incompatibles para la operación solicitada"""
    pass

class InvalidNumericOperationError(NumericCalculationException):
    """Operacion numerica no valida para el tipo de dato o sistema numerico"""
    pass

# ===== File Errors =====
class FileProcessingException(FileOperationException):
    """Excepción general para errores durante el procesamiento de archivos"""
    pass

class FileNameFormatError(FileOperationException):
    """El nombre del archivo no cumple con el formato requerido"""
    pass

class FileNotFoundException(FileOperationException):
    """No se encontro el archivo solicitado en la ruta especificada"""
    pass

class FileReadError(FileOperationException):
    """Error durante la lectura del contenido del archivo"""
    pass

class FileWriteError(FileOperationException):
    """Error durante la escritura de datos en un archivo"""
    pass

class InvalidFileContentError(FileOperationException):
    """El contenido del archivo no cumple con el formato esperado"""
    pass

class IOException(FileOperationException):
    """Error durante operaciones de entrada/salida (lectura/escritura)"""
    pass

# ===== Structural Errors =====
class EmptyStructureException(ProjectBaseException):
    """Operación invalida sobre una estructura de datos vacia"""
    pass

class IndexOutOfBoundsException(ProjectBaseException):
    """Intento de acceso a un indice fuera del rango valido"""
    pass

class InvalidDataTypeException(ProjectBaseException):
    """Tipo de dato incompatible con la operacion solicitada"""
    pass