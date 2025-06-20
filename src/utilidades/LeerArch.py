import os
from datetime import datetime
import random



class ArchiveUtil:
    __router = ""

    def __init__(self, router=os.getcwd()):
        if not router or len(router) == 0:
            raise ValueError("Manage-Error: La ruta es vacia")
        self.utilDirectory(router)

    def getRouter(self) -> str:
        return str(self.__router)
    
    def getArchive(self, nameArchive: str):
        if not nameArchive or len(nameArchive) == 0:
            raise ValueError("Manage-Error: El nombre esta Vacio")
        
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
            print(f"Manage-Error: La ruta '{self.__router}' no es un directorio")
            return []
        except Exception as e:
            print(f"Manage-Error: Ocurrio un error inesperado al listar el directorio: {e}")
            return []
        
    def setRouter(self, router: str):
        if not router or len(router) == 0:
            raise ValueError("Manage-Error: La ruta es vacia")
        self.utilDirectory(router)

    def utilDirectory(self, router: str):
        if not os.path.exists(router):
            raise FileNotFoundError(f"Manage-Error: El directorio '{router}' no existe")
        if not os.path.isdir(router):
            raise NotADirectoryError(f"Manage-Error: La ruta '{router}' no es un directorio")
        self.__router = router


class arregloBidimensional:
    def __init__(self):
        self.filas = {}
        self.maxColumna = -1

    def agregarElemento(self, fila: int, columna: int, valor: str):
        if fila < 0 or columna < 0:
            raise ValueError("Las coordenadas de fila y columna deben ser no negativas")
        
        if fila not in self.filas:
            self.filas[fila] = {}
        self.filas[fila][columna] = valor
        if columna > self.maxColumna:
            self.maxColumna = columna

    def dimensiones(self) -> tuple[int, int]:
        if not self.filas:
            return (0, 0)
        
        numFilas = max(self.filas.keys()) + 1
        numColumnas = self.maxColumna + 1
        
        return (numFilas, numColumnas)

    def obtenerElemento(self, fila: int, columna: int):
        if fila in self.filas and columna in self.filas[fila]:
            return self.filas[fila][columna]
        return None
    
    def toListOfLists(self) -> list[list[str]]:
        numFilas, numCols = self.dimensiones()
        
        if numFilas == 0:
            return []

        matrizLista = [[None for _ in range(numCols)] for _ in range(numFilas)]
        
        for rIdx, colsDict in self.filas.items():
            for cIdx, value in colsDict.items():
                matrizLista[rIdx][cIdx] = value
                
        return matrizLista


class fileHandler(ArchiveUtil):
    def __init__(self, rutaArchivo: str):
        directorio = os.path.dirname(rutaArchivo)
        if not directorio:
            directorio = os.getcwd()
        super().__init__(directorio)
        
        self.nombreArchivo = os.path.basename(rutaArchivo)
        self.matrizDatos = self.leerArchivo()
        
    def leerArchivo(self) -> arregloBidimensional:
        matriz = arregloBidimensional()
        try:
            with self.getArchive(self.nombreArchivo) as archivoBin:
               
                for i, lineaBytes in enumerate(archivoBin):
                    try:
                        linea = lineaBytes.decode('utf-8').strip()
                    except UnicodeDecodeError:
                        print(f"Advertencia: No se pudo decodificar la linea {i+1} del archivo '{self.nombreArchivo}'. Se omitira")
                        continue 

                    if not linea:
                        continue

                    valores = linea.split('#')
                    for j, valorStr in enumerate(valores):
                        valorLimpio = valorStr.strip()

                        if valorLimpio: 
                            if self.esOctal(valorLimpio):
                                matriz.agregarElemento(i, j, f"Ocho: {valorLimpio}")
                            elif not self.esReconocido(valorLimpio):
                                matriz.agregarElemento(i, j, f"{valorLimpio}")
                            else:
                                matriz.agregarElemento(i, j, valorLimpio)

        except Exception as e:
            print(f"Error en lectura o procesamiento del archivo '{self.nombreArchivo}': {e}")
            return arregloBidimensional()
        return matriz
    
    def esOctal(self, valor: str) -> bool:
        if not isinstance(valor, str) or not valor:
            return False
        
        if '.' in valor:
            return False

        esSoloOctalDigitos = all(c in '01234567' for c in valor)
        
        if esSoloOctalDigitos:
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
        
    def esReconocido(self, valor: str) -> bool:
        def esBinarioUtil(val: str) -> bool:
            return all(c in '01.' for c in val)

        def esDecimalUtil(val: str) -> bool:
            partes = val.split('.')
            if len(partes) > 2:
                return False
            return all(part.isdigit() for part in partes)

        def esHexadecimalUtil(val: str) -> bool:
            return all(c in '0123456789abcdefABCDEF.' for c in val)
            
        valorLower = valor.lower()
        return esBinarioUtil(valorLower) or esDecimalUtil(valorLower) or esHexadecimalUtil(valorLower)

    def get_dimensiones(self) -> tuple[int, int]:
        return self.matrizDatos.dimensiones()
    
    def get_datos(self) -> arregloBidimensional:
        return self.matrizDatos


class lectorArchivosBin:
    def __init__(self, rutaCarpetaArchivosBin: str):
        self.rutaCarpetaArchivosBin = rutaCarpetaArchivosBin
        
        if not os.path.isdir(self.rutaCarpetaArchivosBin):
            raise FileNotFoundError(f"La carpeta de archivos binarios no existe: {rutaCarpetaArchivosBin}")

    def obtenerArchivosParaProcesar(self) -> list[tuple[str, arregloBidimensional]]:
        archiveUtilForListing = ArchiveUtil(self.rutaCarpetaArchivosBin)
        nombresArchivos = archiveUtilForListing.getDirectoriesList()
        
        archivosProcesables = []
        if not nombresArchivos:
            print(f"No se encontraron archivos en la carpeta: {self.rutaCarpetaArchivosBin}")
            return []
            
        for nombreArchivo in nombresArchivos:
            if nombreArchivo.endswith('.bin'):
                rutaCompletaArchivoBin = os.path.join(self.rutaCarpetaArchivosBin, nombreArchivo)
                fileHandler = fileHandler(rutaCompletaArchivoBin)
                matrizDatos = fileHandler.getDatos()
                
                if matrizDatos.dimensiones() == (0, 0):
                    print(f"Advertencia: El archivo '{fileHandler.nombreArchivo}' esta vacio o contiene datos invalidos, se saltara")
                else:
                    archivosProcesables.append((fileHandler.nombreArchivo, matrizDatos))
            else:
                print(f"Saltando archivo no .bin: {nombreArchivo}")
        
        return archivosProcesables