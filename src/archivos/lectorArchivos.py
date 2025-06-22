from estructuras.LinkedList import LinkedList
from numeros.Binary import Binary
from numeros.Decimal import Decimal
from numeros.Hexadecimal import Hexadecimal
from utilidades.FormatValidator import FormatValidator
from errores.CustomExceptions import InvalidNumberFormatException, FileNameFormatException

class FileReader:
    def __init__(self):
        """
        Inicializa el lector de archivos con estructuras de datos propias
        """
        self.data = LinkedList()
        self.errorList = LinkedList()
        self.rowCount = 0
        self.columnCount = 0
    
    def processFile(self, filePath: str) -> LinkedList:
        """
        Procesa un archivo de texto y devuelve los datos estructurados
        
        Args:
            filePath: Ruta completa al archivo
            
        Returns:
            LinkedList con los datos procesados
            
        Raises:
            FileNotFoundException: Si el archivo no existe
            IOException: Si hay errores de lectura
            FileNameFormatException: Si el nombre no cumple el formato
        """
        # Obtener nombre del archivo de la ruta
        fileName = self.extractFileName(filePath)
        
        # Validar formato del nombre
        if not FormatValidator.validateFileNameFormat(fileName):
            raise FileNameFormatException(f"Invalid file name format: {fileName}")
        
        # Leer archivo a cola de líneas
        lineQueue = self.readFileToQueue(filePath)
        
        # Procesar todas las líneas
        self.processLines(lineQueue)
        
        return self.data
    
    def extractFileName(self, path: str) -> str:
        """
        Extrae el nombre del archivo de una ruta completa
        
        Args:
            path: Ruta completa al archivo
            
        Returns:
            Nombre del archivo con extensión
        """
        # Implementación con estructuras propias
        pathParts = LinkedList()
        currentPart = ""
        
        for char in path:
            if char in ['/', '\\']:
                if currentPart:
                    pathParts.add(currentPart)
                    currentPart = ""
            else:
                currentPart += char
        
        if currentPart:
            pathParts.add(currentPart)
        
        return pathParts.getLast() if pathParts.size() > 0 else ""
    
    def readFileToQueue(self, filePath: str) -> LinkedList:
        """
        Lee el archivo y devuelve sus líneas en una cola
        
        Args:
            filePath: Ruta al archivo
            
        Returns:
            Cola de líneas del archivo
        """
        lineQueue = LinkedList()
        
        try:
            # Usar administrador de contexto para garantizar cierre
            with open(filePath, 'r', encoding='utf-8') as file:
                # Leer línea por línea usando estructuras propias
                while True:
                    lineContent = file.readline()
                    if not lineContent:
                        break
                    cleanedLine = lineContent.strip()
                    if cleanedLine:
                        lineQueue.add(cleanedLine)
        except FileNotFoundError:
            raise FileNotFoundException(f"File not found: {filePath}")
        except IOError as ioError:
            raise IOException(f"Read error: {str(ioError)}")
        
        return lineQueue
    
    def processLines(self, lineQueue: LinkedList):
        """
        Procesa todas las líneas de la cola
        
        Args:
            lineQueue: Cola de líneas a procesar
        """
        currentLine = lineQueue.getFirst()
        lineNumber = 1
        
        while currentLine:
            row = self.processLine(currentLine.data, lineNumber)
            
            # Actualizar contadores de dimensiones
            if row.size() > self.columnCount:
                self.columnCount = row.size()
            if row.size() > 0:
                self.data.add(row)
                self.rowCount += 1
            
            currentLine = currentLine.next
            lineNumber += 1
    
    def processLine(self, lineContent: str, lineNumber: int) -> LinkedList:
        """
        Procesa una línea individual y devuelve sus datos
        
        Args:
            lineContent: Contenido de la línea
            lineNumber: Número de línea para reporte de errores
            
        Returns:
            Fila de datos procesados
        """
        row = LinkedList()
        fieldQueue = self.splitFields(lineContent)
        currentField = fieldQueue.getFirst()
        
        while currentField:
            data = currentField.data
            if data:
                try:
                    number = self.createNumber(data)
                    row.add(number)
                except InvalidNumberFormatException as formatError:
                    self.registerError(lineNumber, data, str(formatError))
            currentField = currentField.next
        
        return row
    
    def splitFields(self, lineContent: str) -> LinkedList:
        """
        Divide una línea en campos usando '#' como separador
        
        Args:
            lineContent: Contenido de la línea
            
        Returns:
            Cola de campos
        """
        fieldQueue = LinkedList()
        currentField = ""
        
        for char in lineContent:
            if char == '#':
                if currentField:
                    fieldQueue.add(currentField.strip())
                    currentField = ""
            else:
                currentField += char
        
        if currentField:
            fieldQueue.add(currentField.strip())
        
        return fieldQueue
    
    def createNumber(self, value: str):
        """
        Crea un objeto numérico según el tipo de dato
        
        Args:
            value: Valor numérico en cadena
            
        Returns:
            Instancia de Binary, Decimal o Hexadecimal
            
        Raises:
            InvalidNumberFormatException: Si el formato no es válido
        """
        normalizedValue = value.replace(',', '.').lower()
        
        if FormatValidator.isValidBinary(normalizedValue):
            return Binary(normalizedValue)
        elif FormatValidator.isValidDecimal(normalizedValue):
            return Decimal(normalizedValue)
        elif FormatValidator.isValidHexadecimal(normalizedValue):
            return Hexadecimal(normalizedValue)
        else:
            raise InvalidNumberFormatException("Unrecognized number format")
    
    def registerError(self, lineNumber: int, data: str, message: str):
        """
        Registra un error en el procesamiento
        
        Args:
            lineNumber: Número de línea donde ocurrió
            data: Dato problemático
            message: Mensaje de error
        """
        errorMessage = f"Line {lineNumber}, data '{data}': {message}"
        self.errorList.add(errorMessage)
    
    def getDimensions(self) -> tuple:
        """
        Devuelve las dimensiones del conjunto de datos
        
        Returns:
            Tupla (filas, columnas)
        """
        return (self.rowCount, self.columnCount)
    
    def getErrors(self) -> LinkedList:
        """
        Devuelve la lista de errores encontrados
        
        Returns:
            Lista enlazada de mensajes de error
        """
        return self.errorList