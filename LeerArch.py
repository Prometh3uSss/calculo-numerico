import os

class ArchiveUtil:
    __router = ""

    def __init__(self, router=os.getcwd()):
        if not router or len(router) == 0:
            raise Exception("Manage-Error: La ruta es vacia.")
        self.utilDirectory(router)

    def getRouter(self):
        return str(self.__router)
    
    def getArchive(self, nameArchive):
        if not nameArchive or len(nameArchive) == 0:
            raise Exception("Manage-Error: El nombre esta Vacio.")
        
        try:
            return open(os.path.join(self.__router, nameArchive), 'rb')
        except FileNotFoundError as e:
            print("Manage-Error: El archivo no ha sido encontrado", e)
            return None

    def getDirectoriesList(self):
        try:
            directories = os.listdir(self.__router)
            if len(directories) > 0:
                return directories
            raise FileNotFoundError("No se encontraron archivos.")
        except FileNotFoundError as e:
            print("Manage-Error: Directorio no existe: ", e)
            return None
        except NotADirectoryError as e:
            print("Manage-Error: Ocurrió un error inesperado:", e)
            return None
        
    def setRouter(self, router):
        if not router or len(router) == 0:
            raise Exception("Manage-Error: La ruta es vacia.")
        self.utilDirectory(router)

    def setOrCreateFiles(self, nameArchive, content="", bool=False):
        if not nameArchive or len(nameArchive) == 0:
            raise Exception("Manage-Error: El nombre esta Vacio.")
        
        try:
            if not content or len(content) == 0:
                open(os.path.join(self.__router, nameArchive + ".txt"), 'x')
                return
            
            with open(os.path.join(self.__router, nameArchive), 'a') as archive:
                if bool:
                    archive.write(content + "\n")
                else:
                    archive.write(content)
        except FileNotFoundError as e:
            print("Manage-Error: El archivo no ha sido encontrado", e)

    def utilDirectory(self, router):
        if os.path.exists(router) and not os.path.isdir(router):
            raise NotADirectoryError(f"Manage-Error: La ruta '{router}' no es un directorio.")
        elif not os.path.exists(router):
            raise FileNotFoundError(f"Manage-Error: El directorio '{router}' no existe.")
        self.__router = router

class FileHandler(ArchiveUtil):
    def __init__(self, ruta_archivo: str):
        directorio = os.path.dirname(ruta_archivo) or os.getcwd()
        super().__init__(directorio)
        self.nombre_archivo = os.path.basename(ruta_archivo)
        self.matriz_datos = self._leer_archivo()
    
    def _leer_archivo(self):
        """Lee el archivo binario y retorna un arreglo bidimensional personalizado"""
        try:
            with self.getArchive(self.nombre_archivo) as archivo_bin:
                contenido = archivo_bin.read().decode('utf-8')
                lineas = contenido.split('\n')
                matriz = ArregloBidimensional()
                
                for i, linea in enumerate(lineas):
                    linea_limpia = linea.strip()
                    if not linea_limpia:
                        continue
                    valores = linea_limpia.split('#')
                    for j, valor in enumerate(valores):
                        valor_limpio = valor.strip()
                        if valor_limpio:
                            matriz.agregar_elemento(i, j, valor_limpio)
                
                return matriz
        except Exception as e:
            print(f"Error en lectura de archivo: {e}")
            return ArregloBidimensional()
    
    def get_dimensiones(self):
        """Retorna (filas, columnas) de la matriz de datos"""
        return self.matriz_datos.dimensiones()
    
    def get_datos(self):
        """Retorna la matriz de datos completa"""
        return self.matriz_datos

class ArregloBidimensional:
    """Implementación personalizada de un arreglo bidimensional"""
    def __init__(self):
        self.filas = {}
        self.max_columna = 0
    
    def agregar_elemento(self, fila, columna, valor):
        if fila not in self.filas:
            self.filas[fila] = {}
        self.filas[fila][columna] = valor
        if columna > self.max_columna:
            self.max_columna = columna
    
    def dimensiones(self):
        if not self.filas:
            return (0, 0)
        filas = max(self.filas.keys()) + 1
        columnas = self.max_columna + 1
        return (filas, columnas)
    
    def obtener_elemento(self, fila, columna):
        if fila in self.filas and columna in self.filas[fila]:
            return self.filas[fila][columna]
        return None

# Crear handler (procesa el archivo automáticamente)
handler = FileHandler("mis_datos.bin")

# Obtener matriz de datos
datos = handler.get_datos()

# Recorrer todos los valores
filas, columnas = handler.get_dimensiones()
for i in range(filas):
    for j in range(columnas):
        valor = datos.obtener_elemento(i, j)
        if valor:
            # Procesar cada valor individual aquí
            print(f"Procesando valor en ({i},{j}): {valor}")