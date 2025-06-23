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
    NumberProcessingException,
    FileNameFormatError,
    FileNotFoundException,
    IOException
)

def mainExecution():
    try:
        # 1. Configuración inicial
        dataDirectoryPath = os.path.join(os.getcwd(), 'data')
        outputDirectoryPath = os.path.join(os.getcwd(), 'output')
        
        # 2. Preparar entorno
        setupProcessingEnvironment(outputDirectoryPath)
        
        # 3. Inicializar componentes
        fileProcessor = FileReader()
        fileGenerator = FileGenerator(outputDirectoryPath)
        
        # 4. Obtener archivos a procesar
        filesToProcess = getProcessableFiles(dataDirectoryPath)
        
        if filesToProcess.getListLength() == 0:
            print("No se encontraron archivos validos para procesar en la carpeta 'data'")
            return
        
        # 5. Procesar cada archivo
        processFileCollection(filesToProcess, fileProcessor, fileGenerator)
        
    except Exception as criticalError:
        print(f"Error critico en la ejecucion: {str(criticalError)}")

def setupProcessingEnvironment(outputDirectory: str):
    if not os.path.exists(outputDirectory):
        try:
            os.makedirs(outputDirectory)
            print(f"Directorio de salida creado: {outputDirectory}")
        except OSError as osError:
            raise OSError(f"Error creando directorio: {str(osError)}")

def getProcessableFiles(directoryPath: str) -> LinkedList:
    fileList = LinkedList()
    
    try:
        for fileName in os.listdir(directoryPath):
            if fileName.endswith('.txt'):
                fullPath = os.path.join(directoryPath, fileName)
                fileList.addElementAtEnd(fullPath)
    except FileNotFoundError:
        print(f"Advertencia: Carpeta 'data' no encontrada en {directoryPath}")
    
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
        
        # 1. Leer y procesar archivo
        processedData = fileProcessor.processInputFile(filePath)
        rowCount, columnCount = fileProcessor.getDimensions()
        print(f"Archivo procesado: {rowCount} filas x {columnCount} columnas")
        
        # 2. Calcular resultados numéricos
        analysisResults = LinkedList()
        calculateNumericalAnalysis(processedData, analysisResults)
        
        # 3. Calcular errores
        calculateErrorMetrics(processedData, analysisResults)
        
        # 4. Generar archivo de salida
        baseName = fileName.split('_')[0]
        outputFilePath = fileGenerator.generateOutputFile(baseName, analysisResults)
        
        # 5. Mostrar estadisticas
        displayProcessingStatistics(startTime, outputFilePath, fileProcessor)
        
    except (FileNameFormatError, FileNotFoundException, IOException) as ioError:
        raise FileProcessingException(f"Error de entrada/salida: {str(ioError)}")
    except NumberProcessingException as numError:
        raise FileProcessingException(f"Error numerico: {str(numError)}")
    except Exception as processingError:
        raise FileProcessingException(f"Error procesando {filePath}: {str(processingError)}")

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
        significantDigits = numberObject.getSignificantDigitCount()
        operations = numberObject.getSupportedOperations()
        numberType = getNumberTypeDescription(numberObject)
        
        return (f"Fila {rowIndex}, Col {columnIndex}: "
                f"Valor: {numberObject.getOriginalValue()} | "
                f"Sistema: {numberType} | "
                f"Normalizado: {normalizedForm} | "
                f"Cifras Significativas: {significantDigits} | "
                f"Operaciones: {operations}")
    except Exception as formatError:
        return f"Error formateando resultado: {str(formatError)}"

def getNumberTypeDescription(numberObject) -> str:
    if isinstance(numberObject, Binary):
        return "Binario"
    elif isinstance(numberObject, Decimal):
        return "Decimal"
    elif isinstance(numberObject, Hexadecimal):
        return "Hexadecimal"
    return "Desconocido"

def calculateErrorMetrics(processedData: LinkedList, resultContainer: LinkedList):
    if processedData.getListLength() < 1:
        return
    
    try:
        # Obtener los primeros dos numeros validos
        firstRow = processedData.headNode.elementData
        if firstRow.getListLength() < 2:
            return
            
        firstNumber = firstRow.headNode.elementData
        secondNumber = firstRow.headNode.nextNode.elementData
        
        # Calcular errores usando metodos estaticos
        absoluteError = ErrorCalculator.calculateAbsoluteError(
            firstNumber.convertToDecimal(),
            secondNumber.convertToDecimal()
        )
        
        relativeError = ErrorCalculator.calculateRelativeError(
            firstNumber.convertToDecimal(),
            secondNumber.convertToDecimal()
        )
        
        # Usar 4 digitos significativos como ejemplo
        roundingError = ErrorCalculator.calculateRoundingError(4)
        truncationError = ErrorCalculator.calculateTruncationError(4)
        
        # Propagacion de errores (ejemplo con valores absolutos)
        propagationError = ErrorCalculator.calculateProductErrorPropagation(
            [firstNumber.convertToDecimal(), secondNumber.convertToDecimal()],
            [absoluteError, absoluteError]
        )
        
        # Agregar resultados
        resultContainer.addElementAtEnd("\n=== Resultados de Analisis de Errores ===")
        resultContainer.addElementAtEnd(f"Comparacion: {firstNumber.getOriginalValue()} vs {secondNumber.getOriginalValue()}")
        resultContainer.addElementAtEnd(f"Error Absoluto: {absoluteError}")
        resultContainer.addElementAtEnd(f"Error Relativo: {relativeError}")
        resultContainer.addElementAtEnd(f"Error por Redondeo: {roundingError}")
        resultContainer.addElementAtEnd(f"Error por Truncamiento: {truncationError}")
        resultContainer.addElementAtEnd(f"Error por Propagacion: {propagationError}")
        
    except NumberProcessingException as numError:
        resultContainer.addElementAtEnd(f"Error en calculo de errores: {str(numError)}")
    except Exception as generalError:
        resultContainer.addElementAtEnd(f"Error inesperado en calculo de errores: {str(generalError)}")

def displayProcessingStatistics(startTime: float, outputPath: str, fileProcessor: FileReader):
    processingDuration = time.time() - startTime
    print(f"Archivo procesado en {processingDuration:.4f} segundos")
    print(f"Resultados guardados en: {outputPath}")
    
    # Mostrar errores si los hay
    if not fileProcessor.getErrorLog().isEmpty():
        print("\nErrores encontrados durante el procesamiento:")
        errorNode = fileProcessor.getErrorLog().headNode
        while errorNode:
            print(f"  - {errorNode.elementData}")
            errorNode = errorNode.nextNode

if __name__ == "__main__":
    mainExecution()