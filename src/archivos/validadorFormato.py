import re
from datetime import datetime

class ValidadorFormato:
    @staticmethod
    def validar_nombre_archivo(nombre):
        # Formato: nombre_Fecha_Serial.txt
        patron = r"^(.+)_(\d{8})_(\d+)\.txt$"
        coincidencia = re.match(patron, nombre)
        
        if not coincidencia:
            return False
        
        try:
            fecha_str = coincidencia.group(2)
            datetime.strptime(fecha_str, "%Y%m%d")
            # Validar que el serial sea numérico
            int(coincidencia.group(3))
            return True
        except (ValueError, TypeError):
            return False