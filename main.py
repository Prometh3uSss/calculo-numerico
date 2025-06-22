"""
Punto de entrada principal del sistema de cálculo numérico
Implementa el flujo completo de procesamiento usando estructuras propias
Cumple con los estándares de nomenclatura camelCase y comentarios en español
"""

import os
import time
from estructuras.Stack import Stack
from estructuras.LinkedList import LinkedList
from archivos.FileReader import FileReader
from utilidades.FileGenerator import FileGenerator
from numeros.Binary import Binary
from numeros.Decimal import Decimal
from numeros.Hexadecimal import Hexadecimal
from errores.ErrorCalculator import ErrorCalculator
from errores.CustomExceptions import FileProcessingException, NumberProcessingException

def main():
    """
    Función principal que coordina el flujo completo del programa
    """
    try:
        # 1. Configuración inicial
        dataFolderPath = os.path.join(os.getcwd(), 'data')
        outputFolderPath = os.path.join(os.getcwd(), 'output')
        
        # 2. Preparar entorno
        prepareEnvironment(outputFolderPath)
        
        # 3. Inicializar componentes
        fileReader = FileReader()
        fileGenerator = FileGenerator(outputFolderPath)
        
        # 4. Obtener archivos a procesar
        filesToProcess = getFilesToProcess(dataFolderPath)
        
        if filesToProcess.isEmpty():
            print("No se encontraron archivos válidos para procesar en la carpeta 'data'")
            return
        
        # 5. Procesar cada archivo
        processAllFiles(filesToProcess, fileReader, fileGenerator)
        
    except Exception as generalError:
        print(f"Error crítico en la ejecución: {str(generalError)}")

def prepareEnvironment(outputPath: str):
    """
    Crea el directorio de salida si no existe
    
    Args:
        outputPath: Ruta del directorio de salida
    """
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
        print(f"Directorio de salida creado: {outputPath}")

def getFilesToProcess(folderPath: str) -> LinkedList:
    """
    Obtiene la lista de archivos .txt en la carpeta especificada
    
    Args:
        folderPath: Ruta de la carpeta a escanear
        
    Returns:
        Lista enlazada con rutas completas de archivos
    """
    fileList = LinkedList()
    
    try:
        for fileName in os.listdir(folderPath):
            if fileName.endswith('.txt'):
                fullPath = os.path.join(folderPath, fileName)
                fileList.add(fullPath)
    except FileNotFoundError:
        print(f"Advertencia: La carpeta 'data' no existe en {folderPath}")
    
    return fileList

def processAllFiles(filesToProcess: LinkedList, fileReader: FileReader, fileGenerator: FileGenerator):
    """
    Procesa todos los archivos en la lista
    
    Args:
        filesToProcess: Lista de rutas de archivos
        fileReader: Instancia de FileReader
        fileGenerator: Instancia de FileGenerator
    """
    currentFileNode = filesToProcess.getFirstNode()
    
    while currentFileNode:
        try:
            processSingleFile(currentFileNode.data, fileReader, fileGenerator)
        except FileProcessingException as fileError:
            print(f"Error procesando archivo: {str(fileError)}")
        
        currentFileNode = currentFileNode.next

def processSingleFile(filePath: str, fileReader: FileReader, fileGenerator: FileGenerator):
    """
    Procesa un archivo individual y genera resultados
    
    Args:
        filePath: Ruta completa al archivo
        fileReader: Instancia de FileReader
        fileGenerator: Instancia de FileGenerator
    """
    try:
        startTime = time.time()
        fileName = os.path.basename(filePath)
        
        printHeader(fileName)
        
        # 1. Leer y procesar archivo
        processedData = fileReader.processFile(filePath)
        rowCount, colCount = fileReader.getDimensions()
        print(f"Archivo procesado: {rowCount} filas x {colCount} columnas")
        
        # 2. Calcular resultados
        analysisResults = LinkedList()
        calculateAnalysisResults(processedData, analysisResults)
        
        # 3. Calcular errores
        calculateAllErrors(processedData, analysisResults)
        
        # 4. Generar archivo de salida
        baseName = fileName.split('_')[0]
        outputFilePath = fileGenerator.generateOutputFile(baseName, analysisResults)
        
        # 5. Mostrar estadísticas
        displayProcessingStats(startTime, outputFilePath, fileReader)
        
    except Exception as processingError:
        raise FileProcessingException(f"Error procesando {filePath}: {str(processingError)}")

def printHeader(fileName: str):
    """
    Imprime encabezado para el procesamiento de archivo
    
    Args:
        fileName: Nombre del archivo a procesar
    """
    separator = "=" * 50
    print(f"\n{separator}")
    print(f"Procesando archivo: {fileName}")
    print(f"{separator}")

def calculateAnalysisResults(processedData: LinkedList, resultContainer: LinkedList):
    """
    Calcula los resultados de análisis para cada número
    
    Args:
        processedData: Datos procesados (lista de filas)
        resultContainer: Contenedor para almacenar resultados
    """
    currentRowNode = processedData.getFirstNode()
    rowNumber = 1
    
    while currentRowNode:
        rowData = currentRowNode.data
        currentCellNode = rowData.getFirstNode()
        colNumber = 1
        
        while currentCellNode:
            numberObject = currentCellNode.data
            resultLine = formatAnalysisResult(rowNumber, colNumber, numberObject)
            resultContainer.add(resultLine)
            
            currentCellNode = currentCellNode.next
            colNumber += 1
        
        currentRowNode = currentRowNode.next
        rowNumber += 1

def formatAnalysisResult(row: int, col: int, number) -> str:
    """
    Formatea el resultado de análisis para un número
    
    Args:
        row: Número de fila
        col: Número de columna
        number: Objeto numérico (Binary, Decimal, Hexadecimal)
        
    Returns:
        Cadena formateada con resultados
    """
    try:
        normalizedForm = number.getNormalizedForm()
        significantDigits = number.getSignificantDigitCount()
        operations = number.getSupportedOperations()
        numberType = getNumberTypeName(number)
        
        return (
            f"Fila {row}, Col {col}: "
            f"Valor: {number.getOriginalValue()} | "
            f"Sistema: {numberType} | "
            f"Normalizado: {normalizedForm} | "
            f"Cifras Signif: {significantDigits} | "
            f"Operaciones: {operations}"
        )
    except Exception as formatError:
        return f"Error formateando resultado: {str(formatError)}"

def getNumberTypeName(number) -> str:
    """
    Devuelve el nombre del tipo de número
    
    Args:
        number: Instancia de número
        
    Returns:
        Nombre del tipo (Binario, Decimal, Hexadecimal)
    """
    if isinstance(number, Binary):
        return "Binario"
    elif isinstance(number, Decimal):
        return "Decimal"
    elif isinstance(number, Hexadecimal):
        return "Hexadecimal"
    return "Desconocido"

def calculateAllErrors(processedData: LinkedList, resultContainer: LinkedList):
    """
    Calcula los 5 tipos de errores requeridos
    
    Args:
        processedData: Datos procesados
        resultContainer: Contenedor para agregar resultados de errores
    """
    if processedData.size() < 1:
        return
    
    try:
        # Obtener los primeros dos números para comparación
        firstRow = processedData.getFirstNode().data
        if firstRow.size() < 2:
            return
            
        firstNumber = firstRow.getFirstNode().data
        secondNumber = firstRow.getFirstNode().next.data
        
        # Calcular errores
        errorCalculator = ErrorCalculator(firstNumber, secondNumber)
        absoluteError = errorCalculator.calculateAbsoluteError()
        relativeError = errorCalculator.calculateRelativeError()
        roundingError = errorCalculator.calculateRoundingError()
        truncationError = errorCalculator.calculateTruncationError()
        propagationError = errorCalculator.calculatePropagationError()
        
        # Agregar resultados
        resultContainer.add("\n=== Resultados de Análisis de Errores ===")
        resultContainer.add(f"Comparación: {firstNumber.getOriginalValue()} vs {secondNumber.getOriginalValue()}")
        resultContainer.add(f"Error Absoluto: {absoluteError}")
        resultContainer.add(f"Error Relativo: {relativeError}")
        resultContainer.add(f"Error por Redondeo: {roundingError}")
        resultContainer.add(f"Error por Truncamiento: {truncationError}")
        resultContainer.add(f"Error por Propagación: {propagationError}")
        
    except NumberProcessingException as numError:
        resultContainer.add(f"Error en cálculo de errores: {str(numError)}")
    except Exception as generalError:
        resultContainer.add(f"Error inesperado en cálculo de errores: {str(generalError)}")

def displayProcessingStats(startTime: float, outputPath: str, fileReader: FileReader):
    """
    Muestra estadísticas del procesamiento
    
    Args:
        startTime: Tiempo de inicio del procesamiento
        outputPath: Ruta del archivo generado
        fileReader: Instancia de FileReader para acceder a errores
    """
    # Calcular tiempo de procesamiento
    processingTime = time.time() - startTime
    print(f"Archivo procesado en {processingTime:.4f} segundos")
    print(f"Resultados guardados en: {outputPath}")
    
    # Mostrar errores si los hay
    if not fileReader.getErrors().isEmpty():
        print("\nErrores encontrados durante el procesamiento:")
        errorNode = fileReader.getErrors().getFirstNode()
        while errorNode:
            print(f"  - {errorNode.data}")
            errorNode = errorNode.next

if __name__ == "__main__":
    main()