"""
Lector de archivos con validación de formato completo
Implementa procesamiento de datos con estructuras propias
"""

from estructuras.listaEnlazada import LinkedList
from numeros.binario import Binario
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
            IOException: Si hay errores de lectura
        """
        fileName = self.extractFileNameFromPath(filePath)
        
        # Validar formato del nombre usando FormatValidator
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
                    pathParts.addElementAtEnd(currentSegment)
                    currentSegment = ""
            else:
                currentSegment += char
        
        if currentSegment:
            pathParts.addElementAtEnd(currentSegment)
        
        return pathParts.getElementAtIndex(pathParts.getListLength() - 1) if pathParts.getListLength() > 0 else ""
    
    def readFileLines(self, filePath: str) -> LinkedList:
        """Lee archivo usando solo estructuras propias"""
        linesQueue = LinkedList()
        
        try:
            with open(filePath, 'r', encoding='utf-8') as file:
                currentLine = ""
                while True:
                    char = file.read(1)
                    if not char:
                        break
                    if char == '\n':
                        linesQueue.addElementAtEnd(currentLine.strip())
                        currentLine = ""
                    else:
                        currentLine += char
                
                if currentLine:
                    linesQueue.addElementAtEnd(currentLine.strip())
                    
        except FileNotFoundError:
            raise FileNotFoundException(f"Archivo no encontrado: {filePath}")
        except IOError as ioError:
            raise IOException(f"Error de lectura: {str(ioError)}")
            
        return linesQueue
    
    def processAllLines(self, linesQueue: LinkedList):
        """Procesa todas las líneas del archivo"""
        currentLineNode = linesQueue.headNode
        lineCounter = 1
        
        while currentLineNode:
            processedRow = self.processSingleLine(currentLineNode.elementData, lineCounter)
            
            if processedRow.getListLength() > self.totalColumns:
                self.totalColumns = processedRow.getListLength()
            
            if processedRow.getListLength() > 0:
                self.processedData.addElementAtEnd(processedRow)
                self.totalRows += 1
            
            currentLineNode = currentLineNode.nextNode
            lineCounter += 1
    
    def processSingleLine(self, lineContent: str, lineNumber: int) -> LinkedList:
        """Procesa una línea individual"""
        rowData = LinkedList()
        fields = self.splitFields(lineContent)
        currentFieldNode = fields.headNode
        
        while currentFieldNode:
            rawValue = currentFieldNode.elementData
            if rawValue:
                try:
                    numberObj = self.createNumberObject(rawValue)
                    rowData.addElementAtEnd(numberObj)
                except InvalidNumberFormatError as formatError:
                    self.logError(lineNumber, rawValue, str(formatError))
            currentFieldNode = currentFieldNode.nextNode
        
        return rowData
    
    def splitFields(self, lineContent: str) -> LinkedList:
        """Divide campos usando '#' como separador"""
        fieldList = LinkedList()
        currentField = ""
        
        for char in lineContent:
            if char == '#':
                if currentField:
                    fieldList.addElementAtEnd(currentField.strip())
                    currentField = ""
            else:
                currentField += char
        
        if currentField:
            fieldList.addElementAtEnd(currentField.strip())
            
        return fieldList
    
    def createNumberObject(self, rawValue: str):
        """
        Crea objeto numérico según el tipo detectado
        Usa FormatValidator para determinar el sistema numérico
        """
        normalizedValue = rawValue.replace(',', '.').lower()
        
        # Usar FormatValidator para determinar el sistema numérico
        numberSystem = FormatValidator.determineNumberSystem(normalizedValue)
        
        if numberSystem == "Binario":
            return Binario(normalizedValue)
        elif numberSystem == "Decimal":
            return Decimal(normalizedValue)
        elif numberSystem == "Hexadecimal":
            return Hexadecimal(normalizedValue)
        else:
            raise InvalidNumberFormatError("Formato numérico desconocido")
    
    def logError(self, lineNumber: int, rawData: str, message: str):
        """Registra error en bitácora"""
        errorEntry = f"Línea {lineNumber}, dato '{rawData}': {message}"
        self.errorLog.addElementAtEnd(errorEntry)
    
    def getDimensions(self) -> tuple:
        """Devuelve dimensiones de los datos procesados"""
        return (self.totalRows, self.totalColumns)
    
    def getErrorLog(self) -> LinkedList:
        """Devuelve bitácora de errores"""
        return self.errorLog