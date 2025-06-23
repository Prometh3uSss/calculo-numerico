import re
from datetime import datetime

class FormatValidator:
    @staticmethod
    def validateFileName(fileName: str) -> bool:
        # Patrón: [nombre]_[AAAAMMDD]_[ddd].txt
        fileNamePattern = r"^([a-zA-Z0-9áéíóúÁÉÍÓÚñÑ]+)_(\d{8})_(\d{3})\.txt$"
        patternMatch = re.match(fileNamePattern, fileName)
        
        if not patternMatch:
            return False
        
        try:
            # Extraer componentes
            dateString = patternMatch.group(2)
            serialNumber = patternMatch.group(3)
            
            # Validar fecha (formato AAAAMMDD)
            datetime.strptime(dateString, "%Y%m%d")
            
            # Validar serial (3 dígitos, 001-999)
            serialValue = int(serialNumber)
            if not (1 <= serialValue <= 999):
                return False
                
            return True
            
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def isValidBinary(inputValue: str) -> bool:
        # Permitir signo opcional y punto decimal
        if inputValue.startswith('-') or inputValue.startswith('+'):
            inputValue = inputValue[1:]
        
        # Dividir en parte entera y fraccionaria
        parts = inputValue.split('.')
        if len(parts) > 2:  # Maximo un punto decimal
            return False
        
        # Todos los caracteres deben ser 0, 1 o .
        validChars = '01.'
        return all(char in validChars for char in inputValue)
    
    @staticmethod
    def isValidDecimal(inputValue: str) -> bool:
        # Permitir signo opcional
        if inputValue.startswith('-') or inputValue.startswith('+'):
            inputValue = inputValue[1:]
        
        # Reemplazar comas por puntos para estandarización
        normalizedValue = inputValue.replace(',', '.')
        
        # Dividir en parte entera y fraccionaria
        parts = normalizedValue.split('.')
        if len(parts) > 2:  # Maximo un punto decimal
            return False
        
        # Todas las partes deben ser digitos
        return all(part.isdigit() for part in parts if part)
    
    @staticmethod
    def isValidHexadecimal(inputValue: str) -> bool:
        # Permitir signo opcional
        if inputValue.startswith('-') or inputValue.startswith('+'):
            inputValue = inputValue[1:]
        
        # Convertir a mayusculas para estandarización
        inputValue = inputValue.upper()
        
        # Dividir en parte entera y fraccionaria
        parts = inputValue.split('.')
        if len(parts) > 2:  # Máximo un punto decimal
            return False
        
        # Caracteres validos: 0-9, A-F, y punto
        validChars = '0123456789ABCDEF.'
        return all(char in validChars for char in inputValue)

    @staticmethod
    def determineNumberSystem(inputValue: str) -> str:
        if FormatValidator.isValidBinary(inputValue):
            return "Binario"
        elif FormatValidator.isValidDecimal(inputValue):
            return "Decimal"
        elif FormatValidator.isValidHexadecimal(inputValue):
            return "Hexadecimal"
        return "Desconocido"