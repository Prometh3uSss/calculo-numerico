import re
from datetime import datetime

class validadorFormato:
    @staticmethod
    def validarNombreArchivo(nombre):
        patron = r"^(.+)(\d{8})(\d+)\.txt$"
        coincidencia = re.match(patron, nombre)
        
        if not coincidencia:
            return False
        
        try:
            fechaStr = coincidencia.group(2)
            datetime.strptime(fechaStr, "%Y%m%d")
            return True
        except ValueError:
            return False