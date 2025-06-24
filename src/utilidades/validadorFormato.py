"""
Módulo para validación de formatos de archivos y números
Cumple con los requisitos del proyecto de cálculo numérico
"""

import re
from datetime import datetime
from errores.tiposErrores import FileNameFormatError
from core.tiposUtilidades import allElementsMeet  # Reemplazo personalizado de all()

class FormatValidator:
    @staticmethod
    def validateFileName(fileName: str) -> bool:
        """
        Valida que el nombre de archivo cumpla el formato requerido:
        nombreValor_FechaActual_SerialArchivo.[txt|bin]
        """
        # Patrón: [nombre]_[AAAAMMDD]_[ddd].[txt|bin]
        fileNamePattern = r"^([a-zA-Z0-9áéíóúÁÉÍÓÚñÑ]+)_(\d{8})_(\d{3})\.(txt|bin)$"
        patternMatch = re.match(fileNamePattern, fileName)
        
        if not patternMatch:
            raise FileNameFormatError(f"Formato inválido: {fileName}")
        
        try:
            dateString = patternMatch.group(2)
            serialNumber = patternMatch.group(3)
            fileExtension = patternMatch.group(4)
            
            # Validar fecha (formato AAAAMMDD)
            datetime.strptime(dateString, "%Y%m%d")
            
            # Validar serial (000-999)
            if not (0 <= int(serialNumber) <= 999):
                raise ValueError("Serial fuera de rango")
                
            return True
            
        except (ValueError, TypeError) as validationError:
            raise FileNameFormatError(
                f"Error en '{fileName}': {str(validationError)}"
            ) from validationError
    
    @staticmethod
    def isValidBinary(value: str) -> bool:
        """Valida si una cadena representa un número binario válido"""
        return allElementsMeet(
            value, 
            lambda char: char in '01.'  # Solo caracteres binarios y punto
        )
    
    @staticmethod
    def isValidDecimal(value: str) -> bool:
        """Valida si una cadena representa un número decimal válido"""
        try:
            # Convertir considerando comas como puntos decimales
            float(value.replace(',', '.'))
            return True
        except ValueError:
            return False
    
    @staticmethod
    def isValidHexadecimal(value: str) -> bool:
        """Valida si una cadena representa un número hexadecimal válido"""
        return allElementsMeet(
            value,
            lambda char: char in '0123456789abcdefABCDEF.'  # Caracteres hex y punto
        )
    
    @staticmethod
    def determineNumberSystem(inputValue: str) -> str:
        """
        Determina el sistema numérico de un valor (binario, decimal, hexadecimal)
        """
        if FormatValidator.isValidBinary(inputValue):
            return "Binary"
        elif FormatValidator.isValidDecimal(inputValue):
            return "Decimal"
        elif FormatValidator.isValidHexadecimal(inputValue):
            return "Hexadecimal"
        return "Desconocido"