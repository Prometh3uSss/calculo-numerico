class ProjectBaseException(Exception):
    """Excepción base para todos los errores personalizados del proyecto"""
    pass

class NumericCalculationException(ProjectBaseException):
    """Clase base para errores relacionados con cálculos numéricos"""
    pass

class FileOperationException(ProjectBaseException):
    """Clase base para errores relacionados con operaciones de archivos"""
    pass

# ===== Numeric Errors =====
class DivisionByZeroError(NumericCalculationException):
    """Se intentó realizar una división donde el denominador es cero"""
    pass

class MathematicalIndeterminacyError(NumericCalculationException):
    """Operación matemática con resultado indeterminado (0/0, ∞/∞, etc.)"""
    pass

class NumericOverflowError(NumericCalculationException):
    """El resultado de un cálculo excede el rango numérico representable"""
    pass

class NumericUnderflowError(NumericCalculationException):
    """El resultado de un cálculo es un número demasiado pequeño para ser representado"""
    pass

class InvalidNumberFormatError(NumericCalculationException):
    """El formato de un número no coincide con el sistema numérico esperado"""
    pass

class MatrixDimensionsError(NumericCalculationException):
    """Las dimensiones de las matrices son incompatibles para la operación solicitada"""
    pass

class InvalidNumericOperationError(NumericCalculationException):
    """Operación numérica no válida para el tipo de dato o sistema numérico"""
    pass

# ===== File Errors =====
class FileNameFormatError(FileOperationException):
    """El nombre del archivo no cumple con el formato requerido"""
    pass

class FileNotFoundException(FileOperationException):
    """No se encontró el archivo solicitado en la ruta especificada"""
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

# ===== Structural Errors =====
class EmptyStructureException(ProjectBaseException):
    """Operación inválida sobre una estructura de datos vacía"""
    pass

class IndexOutOfBoundsException(ProjectBaseException):
    """Intento de acceso a un índice fuera del rango válido"""
    pass

class InvalidDataTypeException(ProjectBaseException):
    """Tipo de dato incompatible con la operación solicitada"""
    pass