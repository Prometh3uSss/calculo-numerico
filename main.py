import os
import time
from estructuras.listaEnlazada import LinkedList
from archivos.lectorArchivos import FileReader
from utilidades.Generador import FileGenerator
from numeros.decimal import Decimal
from numeros.binario import Binary
from numeros.hexadecimal import Hexadecimal
from errores.calculadoraErrores import ErrorCalculator
from errores.tiposErrores import (
    FileProcessingException,
    FileNameFormatError,
    FileNotFoundException,
    IOException
)
from core.tiposUtilidades import isTypeInstance
import numeros

def mainExecution():
    try:
        dataDirectoryPath = os.path.join(os.getcwd(), 'data')
        outputDirectoryPath = os.path.join(os.getcwd(), 'output')
        
        setupProcessingEnvironment(outputDirectoryPath)
        
        fileProcessor = FileReader()
        fileGenerator = FileGenerator(outputDirectoryPath)
        
        filesToProcess = getProcessableFiles(dataDirectoryPath)
        
        if filesToProcess.getListLength() == 0:
            print("No se encontraron archivos válidos para procesar en la carpeta 'data'")
            return
        
        processFileCollection(filesToProcess, fileProcessor, fileGenerator)
        
    except Exception as criticalError:
        print(f"Error critico de ejecucion: {str(criticalError)}")

def setupProcessingEnvironment(outputDirectory: str):
    if not os.path.exists(outputDirectory):
        try:
            os.makedirs(outputDirectory)
            print(f"Directorio de salida creado: {outputDirectory}")
        except OSError as osError:
            raise OSError(f"Error al crear el directorio: {str(osError)}")

def getProcessableFiles(directoryPath: str) -> LinkedList:
    fileList = LinkedList()
    
    try:
        for fileName in os.listdir(directoryPath):
            if fileName.endswith('.txt') or fileName.endswith('.bin'):
                fullPath = os.path.join(directoryPath, fileName)
                fileList.addElementAtEnd(fullPath)
    except FileNotFoundError:
        print(f"Advertencia: no se encontro la carpeta 'data' en {directoryPath}")
    
    return fileList

def processFileCollection(fileList: LinkedList, fileProcessor: FileReader, fileGenerator: FileGenerator):
    currentNode = fileList.headNode
    
    while currentNode:
        try:
            processSingleInputFile(currentNode.elementData, fileProcessor, fileGenerator)
        except FileProcessingException as fileError:
            print(f"Error procesando archivo: {str(fileError)}")
        except Exception as unexpectedError:
            print(f"Error inesperado: {str(unexpectedError)}")
        
        currentNode = currentNode.nextNode

def processSingleInputFile(filePath: str, fileProcessor: FileReader, fileGenerator: FileGenerator):
    try:
        startTime = time.time()
        fileName = os.path.basename(filePath)
        
        printProcessingHeader(fileName)

        processedData = fileProcessor.processInputFile(filePath)
        rowCount, columnCount = fileProcessor.getDimensions()
        print(f"File processed: {rowCount} rows x {columnCount} columns")
        
        analysisResults = LinkedList()
        calculateNumericalAnalysis(processedData, analysisResults)
        
        calculateErrorMetrics(processedData, analysisResults)
        
        baseName = fileName.split('_')[0]
        outputFilePath = fileGenerator.generateOutputFile(baseName, analysisResults)
        
        displayProcessingStatistics(startTime, outputFilePath, fileProcessor)
        
    except (FileNameFormatError, FileNotFoundException, IOException) as ioError:
        raise FileProcessingException(f"Error de procesamiento: {str(ioError)}")
    except Exception as processingError:
        raise FileProcessingException(f"Error inesperado: {str(processingError)}")

def printProcessingHeader(fileName: str):
    separator = "=" * 50
    print(f"\n{separator}")
    print(f"Procesando archivo: {fileName}")
    print(f"{separator}")

def calculateNumericalAnalysis(processedData: LinkedList, resultContainer: LinkedList):
    currentRowNode = processedData.headNode
    rowNumber = 1
    
    while currentRowNode:
        rowData = currentRowNode.elementData
        currentCellNode = rowData.headNode
        columnNumber = 1
        
        while currentCellNode:
            numberObject = currentCellNode.elementData
            resultLine = formatAnalysisResult(rowNumber, columnNumber, numberObject)
            resultContainer.addElementAtEnd(resultLine)
            
            currentCellNode = currentCellNode.nextNode
            columnNumber += 1
        
        currentRowNode = currentRowNode.nextNode
        rowNumber += 1

def formatAnalysisResult(rowIndex: int, columnIndex: int, numberObject) -> str:
    try:
        normalizedForm = numberObject.getNormalizedForm()
        significantDigits = numberObject.getSignificantDigitsCount()
        operations = numberObject.getSupportedOperations()
        numberType = getNumberTypeDescription(numberObject)
        
        return (f"fila {rowIndex}, Col {columnIndex}: "
                f"Valor: {numberObject.getOriginalValue()} | "
                f"Sistema: {numberType} | "
                f"Normalizado: {normalizedForm} | "
                f"Digitos significativos: {significantDigits} | "
                f"Operations: {operations}")
    except Exception as formatError:
        return f"Error al formatear el resultado: {str(formatError)}"

def getNumberTypeDescription(numberObject) -> str:
    if isTypeInstance(numberObject, "Binary"):
        return "Binary"
    elif isTypeInstance(numberObject, "Decimal"):
        return "Decimal"
    elif isTypeInstance(numberObject, "Hexadecimal"):
        return "Hexadecimal"
    return "Desconocido"

def calculateErrorMetrics(processedData: LinkedList, resultContainer: LinkedList):
    if processedData.getListLength() < 1:
        return
    
    try:
        firstRow = processedData.headNode.elementData
        if firstRow.getListLength() < 2:
            return
            
        firstNumber = firstRow.headNode.elementData
        secondNumber = firstRow.headNode.nextNode.elementData
        
        exactValue = firstNumber.convertToFloat()
        approxValue = secondNumber.convertToFloat()
        
        absoluteError = ErrorCalculator.calculateAbsoluteError(exactValue, approxValue)
        relativeError = ErrorCalculator.calculateRelativeError(exactValue, approxValue)
        
        roundingError = ErrorCalculator.calculateRoundingError(4)
        truncationError = ErrorCalculator.calculateTruncationError(4)
        
        propagationError = ErrorCalculator.calculateProductErrorPropagation(
            [exactValue, approxValue],
            [absoluteError, absoluteError]
        )
        
        # Add results
        resultContainer.addElementAtEnd("\n=== Resultados del analisis de ===")
        resultContainer.addElementAtEnd(f"Comparacion: {firstNumber.getOriginalValue()} vs {secondNumber.getOriginalValue()}")
        resultContainer.addElementAtEnd(f"Error Adsoluto: {absoluteError}")
        resultContainer.addElementAtEnd(f"Error Relativo: {relativeError}")
        resultContainer.addElementAtEnd(f"Error por Redondeo: {roundingError}")
        resultContainer.addElementAtEnd(f"Error por truncamiento: {truncationError}")
        resultContainer.addElementAtEnd(f"Error por propagacion: {propagationError}")
        
    except Exception as generalError:
        resultContainer.addElementAtEnd(f"Error en el calculo de errores: {str(generalError)}")

def displayProcessingStatistics(startTime: float, outputPath: str, fileProcessor: FileReader):
    processingDuration = time.time() - startTime
    print(f"Archivo procesado en: {processingDuration:.4f} segundos")
    print(f"Resultdos guardados en: {outputPath}")
    
    if not fileProcessor.getErrorLog().isEmpty():
        print("\nErrores encontrados durante procesamiento:")
        errorNode = fileProcessor.getErrorLog().headNode
        while errorNode:
            print(f"  - {errorNode.elementData}")
            errorNode = errorNode.nextNode

if __name__ == "__main__":
    mainExecution()