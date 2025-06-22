import os
import random
from datetime import datetime
from ..estructuras.listaEnlazada import LinkedList

class FileGenerator:
    def __init__(self, outputPath: str):
        """
        Inicializa el generador con la ruta de salida
        
        Args:
            outputPath: Directorio donde se guardarán los archivos
        """
        self.outputPath = outputPath
        self.checkDirectory()
    
    def checkDirectory(self):
        """Crea el directorio de salida si no existe"""
        if not os.path.exists(self.outputPath):
            try:
                os.makedirs(self.outputPath)
                print(f"Directorio creado: {self.outputPath}")
            except OSError as e:
                raise OSError(f"No se pudo crear el directorio: {str(e)}")
    
    def generateOutputFile(self, baseName: str, resultsList: LinkedList) -> str:
        """
        Genera un archivo de salida con los resultados del análisis
        
        Args:
            baseName: Parte inicial del nombre del archivo (ej: "entrada")
            resultsList: Lista enlazada con los resultados a escribir
            
        Returns:
            Ruta completa del archivo generado, o None si hubo error
        """
        if not baseName or not resultsList or resultsList.length == 0:
            print("Advertencia: Datos insuficientes para generar archivo")
            return None
        
        # Generar nombre de archivo con formato
        fileName = self.generateFileName(baseName)
        fullPath = os.path.join(self.outputPath, fileName)
        
        try:
            # Escribir resultados usando estructuras propias
            self.writeResults(fullPath, resultsList)
            return fullPath
        except Exception as e:
            print(f"Error al generar archivo {fileName}: {str(e)}")
            return None
    
    def generateFileName(self, baseName: str) -> str:
        """
        Genera un nombre de archivo con formato: nombre_Fecha_Serial.txt
        
        Args:
            baseName: Parte inicial del nombre
            
        Returns:
            Nombre de archivo completo
        """
        currentDate = datetime.now().strftime("%Y%m%d")
        serialNumber = random.randint(1, 9999)  # Serial de 1 a 9999
        return f"{baseName}{currentDate}{serialNumber:04d}.txt"
    
    def writeResults(self, filePath: str, resultsList: LinkedList):
        """
        Escribe los resultados en un archivo usando estructuras propias
        
        Args:
            filePath: Ruta completa del archivo a escribir
            resultsList: Lista enlazada con los resultados
        """
        # Usamos un nodo temporal para recorrer la lista
        currentNode = resultsList.head
        
        with open(filePath, 'w', encoding='utf-8') as outputFile:
            while currentNode:
                # Escribir cada resultado en una línea
                outputFile.write(currentNode.data + "\n")
                currentNode = currentNode.next
