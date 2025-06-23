import os
import random
from datetime import datetime
from estructuras.listaEnlazada import LinkedList

class FileGenerator:
    def __init__(self, outputDirectory: str):
        """
        Generador de archivos de salida con formato específico.
        
        Args:
            outputDirectory: Ruta del directorio de salida
            
        Raises:
            OSError: Si no se puede crear el directorio
        """
        self.outputDirectory = outputDirectory
        self.validateOutputDirectory()
    
    def validateOutputDirectory(self):
        """
        Verifica y crea el directorio de salida si no existe.
        
        Raises:
            OSError: Si falla la creación del directorio
        """
        if not os.path.exists(self.outputDirectory):
            try:
                os.makedirs(self.outputDirectory)
                print(f"Directorio creado: {self.outputDirectory}")
            except OSError as error:
                raise OSError(f"Error creando directorio: {str(error)}")
    
    def generateOutputFile(self, baseName: str, resultsList: LinkedList) -> str:
        """
        Genera archivo de resultados con formato específico.
        
        Args:
            baseName: Parte inicial del nombre de archivo
            resultsList: Lista enlazada con resultados a escribir
            
        Returns:
            Ruta completa del archivo generado o None en caso de error
            
        Raises:
            ValueError: Si parámetros son inválidos
        """
        if not baseName or not resultsList or resultsList.getListLength() == 0:
            raise ValueError("Datos insuficientes para generar archivo")
        
        fileName = self.generateFileName(baseName)
        fullPath = os.path.join(self.outputDirectory, fileName)
        
        try:
            self.writeResultsToFile(fullPath, resultsList)
            return fullPath
        except Exception as error:
            print(f"Error generando archivo: {str(error)}")
            return None
    
    def generateFileName(self, baseName: str) -> str:
        """
        Genera nombre de archivo con formato: nombre_Fecha_Serial.txt
        
        Args:
            baseName: Parte inicial del nombre
            
        Returns:
            Nombre de archivo completo
        """
        currentDate = datetime.now().strftime("%Y%m%d")
        serialNumber = random.randint(1, 999)  # Serial de 3 dígitos (001-999)
        return f"{baseName}_{currentDate}_{serialNumber:03d}.txt"
    
    def writeResultsToFile(self, filePath: str, resultsList: LinkedList):
        """
        Escribe resultados en archivo usando estructura propia.
        
        Args:
            filePath: Ruta completa del archivo
            resultsList: Lista enlazada con resultados
            
        Raises:
            IOError: Si falla la escritura del archivo
        """
        try:
            with open(filePath, 'w', encoding='utf-8') as outputFile:
                currentNode = resultsList.headNode
                while currentNode:
                    outputFile.write(currentNode.elementData + "\n")
                    currentNode = currentNode.nextNode
        except IOError as ioError:
            raise IOError(f"Error escribiendo archivo: {str(ioError)}")