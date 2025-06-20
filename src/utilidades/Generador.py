import os
from datetime import datetime
import random

class generadorArchivos:
    """
    Clase encargada de generar archivos de texto con los resultados del analisis numerico
    """
    def __init__(self, rutaSalida: str):
        """
        Inicializa el generador con la ruta donde se guardarán los archivos

        Args:
            ruta_salida (str): La ruta del directorio donde se crearan los archivos .txt.
        """
        if not rutaSalida or not os.path.isdir(rutaSalida):
            raise ValueError(f"Error: La ruta de salida '{rutaSalida}' no es válida o no existe")
        self.rutaSalida = rutaSalida

    def generarArchivoSalida(self, nombreBaseOriginal: str, resultados: list[str]) -> str:
        """
        Genera un archivo .txt con los resultados del analisis.

        El nombre del archivo sigue el formato: nombreDelValor_FechaActual_SerialArchivo.txt

        Args:
            nombreBaseOriginal (str): El nombre base del archivo .bin original (ej. "nombreDelValor")
                                         Se usara como prefijo para el nombre del archivo de salida
            resultados (list[str]): Una lista de cadenas, donde cada cadena es una linea de resultado

        Returns:
            str: La ruta completa del archivo generado si la operacion es exitosa, None en caso de error
        """
        fechaActual = datetime.now().strftime("%Y%m%d")
        serial = random.randint(0, 100)
        
        nombreArchivo = f"{nombreBaseOriginal}_{fechaActual}_{serial}.txt"
        rutaCompletaArchivo = os.path.join(self.rutaSalida, nombreArchivo)
        
        try:
            with open(rutaCompletaArchivo, 'w', encoding='utf-8') as archivo:
                for resultado in resultados:
                    archivo.write(resultado + "\n")
            print(f"Archivo de resultados generado: {rutaCompletaArchivo}")
            return rutaCompletaArchivo
        except IOError as e:
            print(f"Error de E/S al generar el archivo '{nombreArchivo}': {e}")
            return None
        except Exception as e:
            print(f"Error inesperado al generar archivo '{nombreArchivo}': {e}")
            return None