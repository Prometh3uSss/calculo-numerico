import os

class FileManager:
    __directoryPath = ""

    def __init__(self, directoryPath=os.getcwd()):
        if not directoryPath or len(directoryPath) == 0:
            raise ValueError("Manage-Error: La ruta es vacia")
        self.useDirectory(directoryPath)

    def getDirectoryPath(self) -> str:
        return str(self.__directoryPath)
    
    def getFile(self, fileName: str):
        if not fileName or len(fileName) == 0:
            raise ValueError("Manage-Error: El nombre esta Vacio")
        
        try:
            return open(os.path.join(self.__directoryPath, fileName), 'rb')
        except FileNotFoundError as error:
            print(f"Manage-Error: El archivo '{fileName}' no ha sido encontrado en '{self.__directoryPath}': {error}")
            return None
        except IOError as error:
            print(f"Manage-Error: Error al acceder al archivo '{fileName}': {error}")
            return None

    def listDirectoryContents(self) -> list:
        try:
            directoryContents = os.listdir(self.__directoryPath)
            if len(directoryContents) > 0:
                return directoryContents
            return [] 
        except FileNotFoundError:
            print(f"Manage-Error: Directorio no existe o no se puede acceder: '{self.__directoryPath}'")
            return []
        except NotADirectoryError:
            print(f"Manage-Error: La ruta '{self.__directoryPath}' no es un directorio")
            return []
        except Exception as error:
            print(f"Manage-Error: Ocurrio un error inesperado al listar el directorio: {error}")
            return []
        
    def setDirectoryPath(self, directoryPath: str):
        if not directoryPath or len(directoryPath) == 0:
            raise ValueError("Manage-Error: La ruta es vacia")
        self.useDirectory(directoryPath)

    def useDirectory(self, directoryPath: str):
        if not os.path.exists(directoryPath):
            raise FileNotFoundError(f"Manage-Error: El directorio '{directoryPath}' no existe")
        if not os.path.isdir(directoryPath):
            raise NotADirectoryError(f"Manage-Error: La ruta '{directoryPath}' no es un directorio")
        self.__directoryPath = directoryPath


class TwoDimensionalArray:
    def __init__(self):
        self.rows = {}
        self.maxColumn = -1

    def addElement(self, row: int, column: int, value: str):
        if row < 0 or column < 0:
            raise ValueError("Las coordenadas de fila y columna deben ser no negativas")
        
        if row not in self.rows:
            self.rows[row] = {}
        self.rows[row][column] = value
        if column > self.maxColumn:
            self.maxColumn = column

    def getDimensions(self) -> tuple[int, int]:
        if not self.rows:
            return (0, 0)
        
        numRows = max(self.rows.keys()) + 1
        numColumns = self.maxColumn + 1
        
        return (numRows, numColumns)

    def getElement(self, row: int, column: int):
        if row in self.rows and column in self.rows[row]:
            return self.rows[row][column]
        return None
    
    def toListOfLists(self) -> list[list[str]]:
        numRows, numColumns = self.getDimensions()
        
        if numRows == 0:
            return []

        matrixList = [[None for _ in range(numColumns)] for _ in range(numRows)]
        
        for rowIndex, columnsDict in self.rows.items():
            for columnIndex, elementValue in columnsDict.items():
                matrixList[rowIndex][columnIndex] = elementValue
                
        return matrixList


class FileHandler(FileManager):
    def __init__(self, filePath: str):
        directory = os.path.dirname(filePath)
        if not directory:
            directory = os.getcwd()
        super().__init__(directory)
        
        self.fileName = os.path.basename(filePath)
        self.dataMatrix = self.readFile()
        
    def readFile(self) -> TwoDimensionalArray:
        matrix = TwoDimensionalArray()
        try:
            with self.getFile(self.fileName) as binaryFile:
               
                for lineIndex, lineBytes in enumerate(binaryFile):
                    try:
                        lineContent = lineBytes.decode('utf-8').strip()
                    except UnicodeDecodeError:
                        print(f"Advertencia: No se pudo decodificar la linea {lineIndex+1} del archivo '{self.fileName}'. Se omitira")
                        continue 

                    if not lineContent:
                        continue

                    values = lineContent.split('#')
                    for columnIndex, rawValue in enumerate(values):
                        cleanValue = rawValue.strip()

                        if cleanValue: 
                            if self.isOctal(cleanValue):
                                matrix.addElement(lineIndex, columnIndex, f"Ocho: {cleanValue}")
                            elif not self.isRecognized(cleanValue):
                                matrix.addElement(lineIndex, columnIndex, f"{cleanValue}")
                            else:
                                matrix.addElement(lineIndex, columnIndex, cleanValue)

        except Exception as error:
            print(f"Error en lectura o procesamiento del archivo '{self.fileName}': {error}")
            return TwoDimensionalArray()
        return matrix
    
    def isOctal(self, value: str) -> bool:
        if not isinstance(value, str) or not value:
            return False
        
        if '.' in value:
            return False

        isOctalDigits = all(char in '01234567' for char in value)
        
        if isOctalDigits:
            if all(char in '01' for char in value):
                return False
            
            try:
                if len(value) > 1 and value.startswith('0'):
                    int(value, 8)
                    return True
                elif len(value) == 1 and value == '0':
                    return False
            except ValueError:
                pass
        return False
        
    def isRecognized(self, value: str) -> bool:
        def isBinary(valueStr: str) -> bool:
            return all(char in '01.' for char in valueStr)

        def isDecimal(valueStr: str) -> bool:
            parts = valueStr.split('.')
            if len(parts) > 2:
                return False
            return all(part.isdigit() for part in parts)

        def isHexadecimal(valueStr: str) -> bool:
            return all(char in '0123456789abcdefABCDEF.' for char in valueStr)
            
        valueLower = value.lower()
        return isBinary(valueLower) or isDecimal(valueLower) or isHexadecimal(valueLower)

    def getDimensions(self) -> tuple[int, int]:
        return self.dataMatrix.getDimensions()
    
    def getData(self) -> TwoDimensionalArray:
        return self.dataMatrix


class BinaryFilesReader:
    def __init__(self, binaryFilesFolderPath: str):
        self.binaryFilesFolderPath = binaryFilesFolderPath
        
        if not os.path.isdir(self.binaryFilesFolderPath):
            raise FileNotFoundError(f"La carpeta de archivos binarios no existe: {binaryFilesFolderPath}")

    def getFilesToProcess(self) -> list[tuple[str, TwoDimensionalArray]]:
        fileManager = FileManager(self.binaryFilesFolderPath)
        fileNames = fileManager.listDirectoryContents()
        
        processableFiles = []
        if not fileNames:
            print(f"No se encontraron archivos en la carpeta: {self.binaryFilesFolderPath}")
            return []
            
        for fileName in fileNames:
            if fileName.endswith('.bin'):
                fullBinaryFilePath = os.path.join(self.binaryFilesFolderPath, fileName)
                fileHandler = FileHandler(fullBinaryFilePath)
                dataMatrix = fileHandler.getData()
                
                if dataMatrix.getDimensions() == (0, 0):
                    print(f"Advertencia: El archivo '{fileHandler.fileName}' esta vacio o contiene datos invalidos, se saltara")
                else:
                    processableFiles.append((fileHandler.fileName, dataMatrix))
            else:
                print(f"Saltando archivo no .bin: {fileName}")
        
        return processableFiles