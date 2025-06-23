import re
from datetime import datetime
from errores.tiposErrores import FileNameFormatError

class FormatValidator:
    @staticmethod
    def validateFileName(fileName: str) -> bool:
        """
        Valida que el nombre de archivo cumpla el formato:
        nombreDelValor_FechaActual_SerialArchivo.txt
        
        Args:
            fileName: Nombre del archivo a validar
            
        Returns:
            True si cumple formato, False en caso contrario
            
        Raises:
            FileNameFormatError: Si el formato es inválido
        """
        # Patrón mejorado con serial de 3 dígitos
        fileNamePattern = r"^([a-zA-Z0-9áéíóúÁÉÍÓÚñÑ]+)_(\d{8})_(\d{3})\.txt$"
        patternMatch = re.match(fileNamePattern, fileName)
        
        if not patternMatch:
            raise FileNameFormatError(f"Formato inválido: {fileName}")
        
        try:
            dateString = patternMatch.group(2)
            serialNumber = patternMatch.group(3)
            
            # Validar fecha
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
        """Valida formato binario (0-1 y punto decimal)"""
        return all(char in '01.' for char in value)
    
    @staticmethod
    def isValidDecimal(value: str) -> bool:
        """Valida formato decimal (dígitos, signo y punto)"""
        try:
            float(value.replace(',', '.'))
            return True
        except ValueError:
            return False
    
    @staticmethod
    def isValidHexadecimal(value: str) -> bool:
        """Valida formato hexadecimal (0-9, A-F, punto)"""
        return all(char in '0123456789abcdefABCDEF.' for char in value)