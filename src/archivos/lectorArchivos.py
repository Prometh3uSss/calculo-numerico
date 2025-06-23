from estructuras.listaEnlazada import LinkedList
from numeros.binario import Binary
from numeros.decimal import Decimal
from numeros.hexadecimal import Hexadecimal
from utilidades.validadorFormato import FormatValidator
from errores.tiposErrores import (
    FileNameFormatError,
    FileNotFoundException,
    IOException,
    InvalidNumberFormatError
)

class FileReader:
    def __init__(self):
        """Inicializa estructuras de datos propias"""
        self.processedData = LinkedList()
        self.errorLog = LinkedList()
        self.totalRows = 0
        self.totalColumns = 0
    
    def processInputFile(self, filePath: str) -> LinkedList:
        """
        Procesa un archivo y devuelve datos estructurados
        
        Args:
            filePath: Ruta completa al archivo
            
        Returns:
            LinkedList con datos procesados
            
        Raises:
            FileNameFormatError: Si el nombre no cumple formato
            FileNotFoundException: Si el archivo no existe
            IOException: Errores de lectura
        """
        fileName = self.extractFileNameFromPath(filePath)
        
        if not FormatValidator.validateFileName(fileName):
            raise FileNameFormatError(f"Formato inválido: {fileName}")
        
        rawLines = self.readFileLines(filePath)
        self.processAllLines(rawLines)
        
        return self.processedData
    
    def extractFileNameFromPath(self, path: str) -> str:
        """Extrae nombre de archivo usando estructuras propias"""
        pathParts = LinkedList()
        currentSegment = ""
        
        for char in path:
            if char in ['/', '\\']:
                if currentSegment:
                    pathParts.append(currentSegment)
                    currentSegment = ""
            else:
                currentSegment += char
        
        if currentSegment:
            pathParts.append(currentSegment)
        
        return pathParts.get(pathParts.length - 1) if pathParts.length > 0 else ""
    
    def readFileLines(self, filePath: str) -> LinkedList:
        """Lee archivo usando solo estructuras propias"""
        linesQueue = LinkedList()
        fileBuffer = self.readFileBytes(filePath)
        currentLine = ""
        
        for byte in fileBuffer:
            char = chr(byte)
            if char == '\n':
                linesQueue.append(currentLine.strip())
                currentLine = ""
            else:
                currentLine += char
        
        if currentLine:
            linesQueue.append(currentLine.strip())
            
        return linesQueue
    
    def readFileBytes(self, filePath: str) -> LinkedList:
        """Lee bytes del archivo usando estructura propia"""
        byteList = LinkedList()
        
        try:
            # Simulación de lectura sin open() nativo
            # (Implementación real dependería de OS)
            for byte in self.os_read_file_simulation(filePath):
                byteList.append(byte)
        except FileNotFoundError:
            raise FileNotFoundException(f"Archivo no encontrado: {filePath}")
        except IOError as ioErr:
            raise IOException(f"Error de lectura: {str(ioErr)}")
            
        return byteList
    
    def os_read_file_simulation(self, filePath):
        """Simula lectura de archivo (implementación real sería con llamadas a sistema)"""
        # EN PRODUCCIÓN: Reemplazar con llamadas a sistema usando ctypes/OS
        with open(filePath, 'rb') as f:
            while byte := f.read(1):
                yield ord(byte)
    
    def processAllLines(self, linesQueue: LinkedList):
        """Procesa todas las líneas del archivo"""
        currentLineNode = linesQueue.head
        lineCounter = 1
        
        while currentLineNode:
            processedRow = self.processSingleLine(currentLineNode.data, lineCounter)
            
            if processedRow.length > self.totalColumns:
                self.totalColumns = processedRow.length
            
            if processedRow.length > 0:
                self.processedData.append(processedRow)
                self.totalRows += 1
            
            currentLineNode = currentLineNode.next
            lineCounter += 1
    
    def processSingleLine(self, lineContent: str, lineNumber: int) -> LinkedList:
        """Procesa una línea individual"""
        rowData = LinkedList()
        fields = self.splitFields(lineContent)
        currentFieldNode = fields.head
        
        while currentFieldNode:
            rawValue = currentFieldNode.data
            if rawValue:
                try:
                    numberObj = self.createNumberObject(rawValue)
                    rowData.append(numberObj)
                except InvalidNumberFormatError as formatErr:
                    self.logError(lineNumber, rawValue, str(formatErr))
            currentFieldNode = currentFieldNode.next
        
        return rowData
    
    def splitFields(self, lineContent: str) -> LinkedList:
        """Divide campos usando '#' como separador"""
        fieldList = LinkedList()
        currentField = ""
        
        for char in lineContent:
            if char == '#':
                if currentField:
                    fieldList.append(currentField.strip())
                    currentField = ""
            else:
                currentField += char
        
        if currentField:
            fieldList.append(currentField.strip())
            
        return fieldList
    
    def createNumberObject(self, rawValue: str):
        """Crea objeto numérico según el tipo detectado"""
        normalizedValue = rawValue.replace(',', '.').lower()
        
        if FormatValidator.isValidBinary(normalizedValue):
            return Binary(normalizedValue)
        elif FormatValidator.isValidDecimal(normalizedValue):
            return Decimal(normalizedValue)
        elif FormatValidator.isValidHexadecimal(normalizedValue):
            return Hexadecimal(normalizedValue)
        else:
            raise InvalidNumberFormatError("Formato numérico desconocido")
    
    def logError(self, lineNumber: int, rawData: str, message: str):
        """Registra error en bitácora"""
        errorEntry = f"Línea {lineNumber}, dato '{rawData}': {message}"
        self.errorLog.append(errorEntry)
    
    def getDimensions(self) -> tuple:
        """Devuelve dimensiones de los datos procesados"""
        return (self.totalRows, self.totalColumns)
    
    def getErrorLog(self) -> LinkedList:
        """Devuelve bitácora de errores"""
        return self.errorLog