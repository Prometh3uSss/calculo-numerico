import os
from datetime import datetime
import random

class GeneradorArchivos:
    """
    Clase encargada de generar archivos de texto con los resultados del análisis numérico.
    """
    def __init__(self, ruta_salida: str):
        """
        Inicializa el generador con la ruta donde se guardarán los archivos.

        Args:
            ruta_salida (str): La ruta del directorio donde se crearán los archivos .txt.
        """
        if not ruta_salida or not os.path.isdir(ruta_salida):
            raise ValueError(f"Error: La ruta de salida '{ruta_salida}' no es válida o no existe.")
        self.ruta_salida = ruta_salida

    def generar_archivo_salida(self, nombre_base_original: str, resultados: list[str]) -> str:
        """
        Genera un archivo .txt con los resultados del análisis.

        El nombre del archivo sigue el formato: nombreDelValor_FechaActual_SerialArchivo.txt

        Args:
            nombre_base_original (str): El nombre base del archivo .bin original (ej. "nombreDelValor").
                                         Se usará como prefijo para el nombre del archivo de salida.
            resultados (list[str]): Una lista de cadenas, donde cada cadena es una línea de resultado.

        Returns:
            str: La ruta completa del archivo generado si la operación es exitosa, None en caso de error.
        """
        fecha_actual = datetime.now().strftime("%Y%m%d")
        serial = random.randint(0, 100)
        
        # Construye el nombre del archivo de salida según el formato especificado
        nombre_archivo = f"{nombre_base_original}_{fecha_actual}_{serial}.txt"
        ruta_completa_archivo = os.path.join(self.ruta_salida, nombre_archivo)
        
        try:
            with open(ruta_completa_archivo, 'w', encoding='utf-8') as archivo:
                for resultado in resultados:
                    archivo.write(resultado + "\n")
            print(f"Archivo de resultados generado: {ruta_completa_archivo}")
            return ruta_completa_archivo
        except IOError as e:
            print(f"Error de E/S al generar el archivo '{nombre_archivo}': {e}")
            return None
        except Exception as e:
            print(f"Error inesperado al generar archivo '{nombre_archivo}': {e}")
            return None