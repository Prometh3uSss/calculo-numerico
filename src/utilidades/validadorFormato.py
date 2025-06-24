import re
from datetime import datetime
from errores.tiposErrores import FileNameFormatError
from core.tiposUtilidades import allElementsMeet

class FormatValidator:
    @staticmethod
    def validateFileName(fileName: str) -> bool:
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
        return allElementsMeet(
            value, 
            lambda char: char in '01.'  # Solo caracteres binarios y punto
        )
    
    @staticmethod
    def isValidDecimal(value: str) -> bool:
        try:
            # Convertir considerando comas como puntos decimales
            float(value.replace(',', '.'))
            return True
        except ValueError:
            return False
    
    @staticmethod
    def isValidHexadecimal(value: str) -> bool:
        return allElementsMeet(
            value,
            lambda char: char in '0123456789abcdefABCDEF.'
        )
    
    @staticmethod
    def determineNumberSystem(inputValue: str) -> str:
        if FormatValidator.isValidBinary(inputValue):
            return "Binary"
        elif FormatValidator.isValidDecimal(inputValue):
            return "Decimal"
        elif FormatValidator.isValidHexadecimal(inputValue):
            return "Hexadecimal"
        return "Desconocido"