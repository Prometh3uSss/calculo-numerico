import os
import numpy as np
from datetime import datetime
import random

from src.numeros.CalculosNumericos import Numero 
#La importación de GeneradorArchivos se realizará en el módulo que orqueste.


class ArchiveUtil:
    __router = ""

    def __init__(self, router=os.getcwd()):
        if not router or len(router) == 0:
            raise ValueError("Manage-Error: La ruta es vacia.")
        self.utilDirectory(router)

    def getRouter(self) -> str:
        return str(self.__router)
    
    def getArchive(self, nameArchive: str):
        if not nameArchive or len(nameArchive) == 0:
            raise ValueError("Manage-Error: El nombre esta Vacio.")
        
        try:
            return open(os.path.join(self.__router, nameArchive), 'rb')
        except FileNotFoundError as e:
            print(f"Manage-Error: El archivo '{nameArchive}' no ha sido encontrado en '{self.__router}': {e}")
            return None
        except IOError as e:
            print(f"Manage-Error: Error al acceder al archivo '{nameArchive}': {e}")
            return None

    def getDirectoriesList(self) -> list:
        try:
            directories = os.listdir(self.__router)
            if len(directories) > 0:
                return directories
            return [] 
        except FileNotFoundError:
            print(f"Manage-Error: Directorio no existe o no se puede acceder: '{self.__router}'")
            return []
        except NotADirectoryError:
            print(f"Manage-Error: La ruta '{self.__router}' no es un directorio.")
            return []
        except Exception as e:
            print(f"Manage-Error: Ocurrio un error inesperado al listar el directorio: {e}")
            return []
        
    def setRouter(self, router: str):
        if not router or len(router) == 0:
            raise ValueError("Manage-Error: La ruta es vacia.")
        self.utilDirectory(router)

    def utilDirectory(self, router: str):
        if not os.path.exists(router):
            raise FileNotFoundError(f"Manage-Error: El directorio '{router}' no existe.")
        if not os.path.isdir(router):
            raise NotADirectoryError(f"Manage-Error: La ruta '{router}' no es un directorio.")
        self.__router = router


class ArregloBidimensional:
    def __init__(self):
        self.filas = {}
        self.max_columna = -1

    def agregar_elemento(self, fila: int, columna: int, valor: str):
        if fila < 0 or columna < 0:
            raise ValueError("Las coordenadas de fila y columna deben ser no negativas.")
        
        if fila not in self.filas:
            self.filas[fila] = {}
        self.filas[fila][columna] = valor
        if columna > self.max_columna:
            self.max_columna = columna

    def dimensiones(self) -> tuple[int, int]:
        if not self.filas:
            return (0, 0)
        
        num_filas = max(self.filas.keys()) + 1
        num_columnas = self.max_columna + 1
        
        return (num_filas, num_columnas)

    def obtener_elemento(self, fila: int, columna: int):
        if fila in self.filas and columna in self.filas[fila]:
            return self.filas[fila][columna]
        return None
    
    def to_list_of_lists(self) -> list[list[str]]:
        num_filas, num_cols = self.dimensiones()
        
        if num_filas == 0:
            return []

        matriz_lista = [[None for _ in range(num_cols)] for _ in range(num_filas)]
        
        for r_idx, cols_dict in self.filas.items():
            for c_idx, value in cols_dict.items():
                matriz_lista[r_idx][c_idx] = value
                
        return matriz_lista


class FileHandler(ArchiveUtil):
    def __init__(self, ruta_archivo: str):
        directorio = os.path.dirname(ruta_archivo)
        if not directorio:
            directorio = os.getcwd()
        super().__init__(directorio)
        
        self.nombre_archivo = os.path.basename(ruta_archivo)
        self.matriz_datos = self._leer_archivo()
        
    def _leer_archivo(self) -> ArregloBidimensional:
        matriz = ArregloBidimensional()
        try:
            with self.getArchive(self.nombre_archivo) as archivo_bin:
                # Usar TextIOWrapper para decodificar línea por línea de un archivo binario
                # Esto es más eficiente en memoria para archivos grandes
                for i, linea_bytes in enumerate(archivo_bin):
                    try:
                        linea = linea_bytes.decode('utf-8').strip()
                    except UnicodeDecodeError:
                        print(f"Advertencia: No se pudo decodificar la línea {i+1} del archivo '{self.nombre_archivo}'. Se omitirá.")
                        continue # Saltar líneas que no se pueden decodificar

                    if not linea:
                        continue

                    valores = linea.split('#')
                    for j, valor_str in enumerate(valores):
                        valor_limpio = valor_str.strip()

                        if valor_limpio: # Asegurar que el valor no esté vacío después del strip
                            if self._es_octal(valor_limpio):
                                matriz.agregar_elemento(i, j, f"Ocho: {valor_limpio}")
                            elif not self._es_reconocido(valor_limpio):
                                matriz.agregar_elemento(i, j, f"{valor_limpio}")
                            else:
                                matriz.agregar_elemento(i, j, valor_limpio)

        except Exception as e:
            print(f"Error en lectura o procesamiento del archivo '{self.nombre_archivo}': {e}")
            return ArregloBidimensional()
        return matriz
    
    def _es_octal(self, valor: str) -> bool:
        if not isinstance(valor, str) or not valor:
            return False
        
        if '.' in valor:
            return False

        es_solo_octal_digitos = all(c in '01234567' for c in valor)
        
        if es_solo_octal_digitos:
            if all(c in '01' for c in valor):
                return False
            
            try:
                if len(valor) > 1 and valor.startswith('0'):
                    int(valor, 8)
                    return True
                elif len(valor) == 1 and valor == '0':
                    return False
            except ValueError:
                pass
        return False
        
    def _es_reconocido(self, valor: str) -> bool:
        def es_binario_util(val: str) -> bool:
            return all(c in '01.' for c in val)

        def es_decimal_util(val: str) -> bool:
            partes = val.split('.')
            if len(partes) > 2:
                return False
            return all(part.isdigit() for part in partes)

        def es_hexadecimal_util(val: str) -> bool:
            return all(c in '0123456789abcdefABCDEF.' for c in val)
            
        valor_lower = valor.lower()
        return es_binario_util(valor_lower) or es_decimal_util(valor_lower) or es_hexadecimal_util(valor_lower)

    def get_dimensiones(self) -> tuple[int, int]:
        return self.matriz_datos.dimensiones()
    
    def get_datos(self) -> ArregloBidimensional:
        return self.matriz_datos


class LectorArchivosBin:
    def __init__(self, ruta_carpeta_archivos_bin: str):
        self.ruta_carpeta_archivos_bin = ruta_carpeta_archivos_bin
        
        if not os.path.isdir(self.ruta_carpeta_archivos_bin):
            raise FileNotFoundError(f"La carpeta de archivos binarios no existe: {ruta_carpeta_archivos_bin}")

    def obtener_archivos_para_procesar(self) -> list[tuple[str, ArregloBidimensional]]:
        archive_util_for_listing = ArchiveUtil(self.ruta_carpeta_archivos_bin)
        nombres_archivos = archive_util_for_listing.getDirectoriesList()
        
        archivos_procesables = []
        if not nombres_archivos:
            print(f"No se encontraron archivos en la carpeta: {self.ruta_carpeta_archivos_bin}")
            return []
            
        for nombre_archivo in nombres_archivos:
            if nombre_archivo.endswith('.bin'):
                ruta_completa_archivo_bin = os.path.join(self.ruta_carpeta_archivos_bin, nombre_archivo)
                file_handler = FileHandler(ruta_completa_archivo_bin)
                matriz_datos = file_handler.get_datos()
                
                if matriz_datos.dimensiones() == (0, 0):
                    print(f"Advertencia: El archivo '{file_handler.nombre_archivo}' está vacío o contiene datos inválidos, se saltará.")
                else:
                    archivos_procesables.append((file_handler.nombre_archivo, matriz_datos))
            else:
                print(f"Saltando archivo no .bin: {nombre_archivo}")
        
        return archivos_procesables