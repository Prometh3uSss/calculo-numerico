import re
from datetime import datetime

class FormatValidator:
    @staticmethod
    def validateFileName(fileName):
        # Formato: nombre_Fecha_Serial.txt
        pattern = r"^(.+)_(\d{8})_(\d+)\.txt$"
        match = re.match(pattern, fileName)
        
        if not match:
            return False
        
        try:
            dateStr = match.group(2)
            datetime.strptime(dateStr, "%Y%m%d")
            # Validar que el serial sea numérico
            int(match.group(3))
            return True
        except (ValueError, TypeError):
            return False