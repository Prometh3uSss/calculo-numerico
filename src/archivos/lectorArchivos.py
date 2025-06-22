from ..estructuras.listaEnlazada import ListaEnlazada
from ..errores.tiposErrores import FormatoNumeroInvalidoError, NombreArchivoError
from .validadorFormato import ValidadorFormato
from ..numeros.binario import Binario
from ..numeros.decimal import Decimal
from ..numeros.hexadecimal import Hexadecimal
from ..estructuras.cola import Cola
import os

class FileReader:
    def __init__(self):
        # ListaEnlazada de filas (cada fila es una ListaEnlazada de números)
        self.dataList = ListaEnlazada()
        # Registro de errores encontrados
        self.errorList = ListaEnlazada()
    
    def processFile(self, filePath: str) -> ListaEnlazada:
        """
        Procesa un archivo de texto con formato específico y devuelve los datos estructurados
        
        Args:
            filePath: Ruta completa al archivo a procesar
            
        Returns:
            ListaEnlazada con los datos procesados (filas de números)
            
        Raises:
            FileNotFoundError: Si el archivo no existe
            IOError: Si hay problemas de lectura
            NombreArchivoError: Si el nombre no cumple con el formato
        """
        # Extraer el nombre del archivo de la ruta
        fileName = os.path.basename(filePath)
        
        # Validar el nombre del archivo
        if not ValidadorFormato.validar_nombre_archivo(fileName):
            raise NombreArchivoError(f"El nombre del archivo '{fileName}' no cumple con el formato requerido")
        
        # Intentar abrir y leer el archivo
        try:
            # Usaremos una cola para leer las líneas
            linesQueue = Cola()
            
            # Abrimos el archivo y leemos línea por línea
            with open(filePath, 'r') as file:
                # Leemos todas las líneas y las encolamos
                for lineContent in file:
                    linesQueue.encolar(lineContent.strip())
            
            # Procesamos cada línea en el orden original
            currentLineNumber = 1
            while not linesQueue.esta_vacia():
                lineContent = linesQueue.desencolar()
                processedRow = self._processLine(lineContent, currentLineNumber)
                
                # Solo agregar filas con datos válidos
                if processedRow.longitud > 0:
                    self.dataList.agregar(processedRow)
                
                currentLineNumber += 1
        
        except FileNotFoundError:
            raise FileNotFoundError(f"El archivo {filePath} no existe")
        except IOError as e:
            raise IOError(f"Error al leer el archivo {filePath}: {str(e)}")
        
        return self.dataList
    
    def _processLine(self, lineContent: str, lineNumber: int) -> ListaEnlazada:
        """
        Procesa una línea individual del archivo
        
        Args:
            lineContent: Cadena con los datos de la línea
            lineNumber: Número de línea para reporte de errores
            
        Returns:
            ListaEnlazada con los números procesados de la línea
        """
        rowList = ListaEnlazada()
        
        # Usamos una cola para procesar los campos
        fieldsQueue = Cola()
        currentField = ""
        
        # Procesar cada carácter para dividir por #
        for character in lineContent:
            if character == '#':
                fieldsQueue.encolar(currentField.strip())
                currentField = ""
            else:
                currentField += character
        
        # Agregar el último campo
        if currentField:
            fieldsQueue.encolar(currentField.strip())
        
        # Procesar cada campo
        while not fieldsQueue.esta_vacia():
            fieldData = fieldsQueue.desencolar()
            if not fieldData:  # Ignorar campos vacíos
                continue
                
            try:
                # Determinar el tipo de dato
                numberObject = self._createNumber(fieldData)
                rowList.agregar(numberObject)
            except FormatoNumeroInvalidoError as e:
                # Registrar el error pero continuar procesando
                errorMessage = f"Línea {lineNumber}, dato '{fieldData}': {str(e)}"
                self.errorList.agregar(errorMessage)
        
        return rowList
    
    def _createNumber(self, valueStr: str):
        """
        Crea un objeto numérico según el formato del valor
        
        Args:
            valueStr: Cadena con el valor numérico
            
        Returns:
            Instancia de Binario, Decimal o Hexadecimal
            
        Raises:
            FormatoNumeroInvalidoError: Si el formato no es reconocido
        """
        # Normalizar comas a puntos
        normalizedValue = valueStr.replace(',', '.')
        
        # Determinar el tipo de número
        if self._isBinary(normalizedValue):
            return Binario(normalizedValue)
        elif self._isDecimal(normalizedValue):
            return Decimal(normalizedValue)
        elif self._isHexadecimal(normalizedValue):
            return Hexadecimal(normalizedValue)
        else:
            raise FormatoNumeroInvalidoError(f"Formato numérico no reconocido: {valueStr}")
    
    @staticmethod
    def _isBinary(valueStr: str) -> bool:
        """Verifica si el valor es un número binario válido"""
        # Debe contener solo 0, 1 y un solo punto decimal
        if any(char not in '01.' for char in valueStr):
            return False
        
        # Solo puede haber un punto decimal
        if valueStr.count('.') > 1:
            return False
            
        # Caso especial: solo punto decimal no es válido
        if valueStr == '.':
            return False
            
        return True
    
    @staticmethod
    def _isDecimal(valueStr: str) -> bool:
        """Verifica si el valor es un número decimal válido"""
        # Debe contener solo dígitos y un punto decimal
        parts = valueStr.split('.')
        
        # Solo puede haber un punto decimal
        if len(parts) > 2:
            return False
            
        # Todas las partes deben ser dígitos
        for part in parts:
            if not part.isdigit() and part != '':
                return False
                
        # Caso especial: solo punto decimal no es válido
        if valueStr == '.':
            return False
            
        return True
    
    @staticmethod
    def _isHexadecimal(valueStr: str) -> bool:
        """Verifica si el valor es un número hexadecimal válido"""
        # Debe contener solo dígitos hex, letras A-F y punto decimal
        validChars = "0123456789abcdefABCDEF."
        if any(char not in validChars for char in valueStr):
            return False
        
        # Solo puede haber un punto decimal
        if valueStr.count('.') > 1:
            return False
            
        # Caso especial: solo punto decimal no es válido
        if valueStr == '.':
            return False
            
        return True

    def getErrors(self) -> ListaEnlazada:
        """Devuelve la lista de errores encontrados durante el procesamiento"""
        return self.errorList