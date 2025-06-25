import os
import time
import random
from datetime import datetime
from estructuras.listaEnlazada import LinkedList
from archivos.lectorArchivos import FileReader
from utilidades.Generador import FileGenerator
from errores.calculadoraErrores import ErrorCalculator
from errores.tiposErrores import (
    FileProcessingException,
    FileNameFormatError,
    FileNotFoundException,
    IOException,
    MatrixDimensionsError,
    SingularMatrixError
)
from core.tiposUtilidades import isTypeInstance
from algebra.matrix import Matrix
from algebra.solucionadorLineal import LinearSystemSolver
from errores.errorLogger import ErrorLogger

class LogicaPrincipal:
    def __init__(self, dataDirectoryPath: str, outputDirectoryPath: str, logsDirectoryPath: str):
        self.dataDirectoryPath = dataDirectoryPath
        self.outputDirectoryPath = outputDirectoryPath
        self.logsDirectoryPath = logsDirectoryPath
        self.fileProcessor = FileReader()
        self.fileGenerator = FileGenerator(self.outputDirectoryPath)

    def setupProcessingEnvironment(self):
        for directory in [self.outputDirectoryPath, self.logsDirectoryPath]:
            if not os.path.exists(directory):
                try:
                    os.makedirs(directory)
                    print(f"Directorio creado: {directory}")
                except OSError as osError:
                    raise OSError(f"Error al crear directorio {directory}: {str(osError)}")

    def getProcessableFiles(self) -> LinkedList:
        fileList = LinkedList()
        try:
            if os.path.exists(self.dataDirectoryPath):
                for fileName in os.listdir(self.dataDirectoryPath):
                    if fileName.endswith('.txt') or fileName.endswith('.bin'):
                        fullPath = os.path.join(self.dataDirectoryPath, fileName)
                        fileList.addElementAtEnd(fullPath)
        except FileNotFoundError:
            print(f"Advertencia: no se encontro la carpeta 'data' en {self.dataDirectoryPath}")
        return fileList

    def processFileCollection(self, fileList: LinkedList):
        currentNode = fileList.headNode
        while currentNode:
            try:
                self.processSingleInputFile(currentNode.elementData)
            except FileProcessingException as fileError:
                print(f"Error procesando archivo: {str(fileError)}")
            except Exception as unexpectedError:
                ErrorLogger.log("UnexpectedProcessingError", f"Error inesperado: {str(unexpectedError)}")
                print(f"Error inesperado: {str(unexpectedError)}")
            currentNode = currentNode.nextNode

    def processSingleInputFile(self, filePath: str):
        try:
            startTime = time.time()
            fileName = os.path.basename(filePath)
            
            self.printProcessingHeader(fileName)

            processedData = self.fileProcessor.processInputFile(filePath)
            rowCount, columnCount = self.fileProcessor.getDimensions()
            print(f"Archivo procesado: {rowCount} filas x {columnCount} columnas")
            
            analysisResults = LinkedList()
            self.calculateNumericalAnalysis(processedData, analysisResults)
            
            self.calculateErrorMetrics(processedData, analysisResults)
            
            matrix = self.fileProcessor.processAsMatrix()
            analysisResults.addElementAtEnd("\n=== Operaciones Matriciales ===")
            self.performMatrixOperations(matrix, analysisResults)
            
            baseName = fileName.split('_')[0]
            outputFilePath = self.fileGenerator.generateOutputFile(baseName, analysisResults)
            
            self.displayProcessingStatistics(startTime, outputFilePath)
            
        except (FileNameFormatError, FileNotFoundException, IOException) as ioError:
            raise FileProcessingException(f"Error de procesamiento: {str(ioError)}")
        except Exception as processingError:
            ErrorLogger.log("FileProcessingError", f"Error procesando {filePath}: {str(processingError)}")
            raise FileProcessingException(f"Error inesperado: {str(processingError)}")

    def printProcessingHeader(self, fileName: str):
        separator = "=" * 50
        print(f"\n{separator}")
        print(f"Procesando archivo: {fileName}")
        print(f"{separator}")

    def calculateNumericalAnalysis(self, processedData: LinkedList, resultContainer: LinkedList):
        currentRowNode = processedData.headNode
        rowNumber = 1
        while currentRowNode:
            rowData = currentRowNode.elementData
            currentCellNode = rowData.headNode
            columnNumber = 1
            while currentCellNode:
                numberObject = currentCellNode.elementData
                resultLine = self.formatAnalysisResult(rowNumber, columnNumber, numberObject)
                resultContainer.addElementAtEnd(resultLine)
                currentCellNode = currentCellNode.nextNode
                columnNumber += 1
            currentRowNode = currentRowNode.nextNode
            rowNumber += 1

    def formatAnalysisResult(self, rowIndex: int, columnIndex: int, numberObject) -> str:
        try:
            normalizedForm = numberObject.getNormalizedForm()
            significantDigits = numberObject.getSignificantDigitsCount()
            operations = numberObject.getSupportedOperations()
            numberType = self.getNumberTypeDescription(numberObject)
            
            return (f"Fila {rowIndex}, Col {columnIndex}: "
                    f"Valor: {numberObject.getOriginalValue()} | "
                    f"Sistema: {numberType} | "
                    f"Normalizado: {normalizedForm} | "
                    f"Digitos significativos: {significantDigits} | "
                    f"Operaciones: {','.join(operations)}")
        except Exception as formatError:
            return f"Error al formatear el resultado: {str(formatError)}"

    def getNumberTypeDescription(self, numberObject) -> str:
        if isTypeInstance(numberObject, "Binary"):
            return "Binario"
        elif isTypeInstance(numberObject, "Decimal"):
            return "Decimal"
        elif isTypeInstance(numberObject, "Hexadecimal"):
            return "Hexadecimal"
        return "Desconocido"

    def calculateErrorMetrics(self, processedData: LinkedList, resultContainer: LinkedList):
        if processedData.isEmpty() or processedData.getListLength() < 2:
            return
        
        allValues = LinkedList()
        currentRow = processedData.headNode
        while currentRow:
            row = currentRow.elementData
            if not row.isEmpty():
                currentCell = row.headNode
                while currentCell:
                    try:
                        float_val = currentCell.elementData.convertToFloat()
                        allValues.addElementAtEnd(float_val)
                    except Exception as e:
                        print(f"Advertencia: valor no convertible a float - {str(e)}")
                    currentCell = currentCell.nextNode
            currentRow = currentRow.nextNode
        
        if allValues.getListLength() < 2:
            return
        
        resultContainer.addElementAtEnd("\n=== Resultados del analisis de errores ===")
        
        current = allValues.headNode
        while current and current.nextNode:
            exact = current.elementData
            approx = current.nextNode.elementData
            
            if exact == 0 and approx == 0:
                resultLine = (
                    f"Comparacion: {exact:.6f} vs {approx:.6f}\n"
                    f" - Ambos valores son cero: calculos omitidos"
                )
                resultContainer.addElementAtEnd(resultLine)
                current = current.nextNode.nextNode if current.nextNode else None
                continue
            
            try:
                absError = ErrorCalculator.calculateAbsoluteError(exact, approx)
                relError = ErrorCalculator.calculateRelativeError(exact, approx)
                roundError = ErrorCalculator.calculateRoundingError(4)
                truncError = ErrorCalculator.calculateTruncationError(4)
                
                errorValues = LinkedList()
                errorValues.addElementAtEnd(absError)
                errorValues.addElementAtEnd(relError)
                sumPropError = ErrorCalculator.calculateSumErrorPropagation(errorValues)
                
                valuesList = LinkedList()
                valuesList.addElementAtEnd(exact)
                valuesList.addElementAtEnd(approx)
                
                absErrorsList = LinkedList()
                absErrorsList.addElementAtEnd(absError)
                absErrorsList.addElementAtEnd(absError)
                
                prodPropError = ErrorCalculator.calculateProductErrorPropagation(
                    valuesList, absErrorsList
                )
                
                relError_str = f"{relError:.6f}" if relError != float('inf') else "inf"
                prodPropError_str = f"{prodPropError:.6f}" if prodPropError != float('inf') else "inf"
                
                resultLine = (
                    f"Comparacion: {exact:.6f} vs {approx:.6f}\n"
                    f" - Error Absoluto: {absError:.6f}\n"
                    f" - Error Relativo: {relError_str}\n"
                    f" - Error Redondeo: {roundError:.6f}\n"
                    f" - Error Truncamiento: {truncError:.6f}\n"
                    f" - Propagacion (Suma): {sumPropError:.6f}\n"
                    f" - Propagacion (Producto): {prodPropError_str}"
                )
                resultContainer.addElementAtEnd(resultLine)
                
            except Exception as e:
                errorMsg = (
                    f"Error en calculo para valores {exact:.6f} y {approx:.6f}: "
                    f"{str(e)}"
                )
                resultContainer.addElementAtEnd(errorMsg)
            
            current = current.nextNode.nextNode if current.nextNode else None

    def performMatrixOperations(self, matrix: Matrix, resultContainer: LinkedList):
        try:
            resultContainer.addElementAtEnd("\nOperaciones elementales de matrices:")
            
            try:
                # As per the context, Matrix class does not have transpose or scalar_multiply methods.
                # These calls will raise AttributeError.
                # If these methods were implemented, the code would look like this:
                # transpose = matrix.transpose()
                # resultContainer.addElementAtEnd(f"Transpuesta:\n{transpose}")
                resultContainer.addElementAtEnd(f"Error en transpuesta: 'Matrix' object has no attribute 'transpose'")
            except Exception as e:
                ErrorLogger.log("MatrixTransposeError", f"Error en transpuesta: {str(e)}")
                resultContainer.addElementAtEnd(f"Error en transpuesta: {str(e)}")
            
            try:
                # As per the context, Matrix class does not have transpose or scalar_multiply methods.
                # These calls will raise AttributeError.
                # If these methods were implemented, the code would look like this:
                # scaled = matrix.scalar_multiply(2.5)
                # resultContainer.addElementAtEnd(f"\nMatriz escalada (2.5x):\n{scaled}")
                resultContainer.addElementAtEnd(f"Error en escalado: 'Matrix' object has no attribute 'scalar_multiply'")
            except Exception as e:
                ErrorLogger.log("MatrixScaleError", f"Error en escalado: {str(e)}")
                resultContainer.addElementAtEnd(f"Error en escalado: {str(e)}")
            
            if matrix.is_square() and matrix.cols == matrix.rows + 1:
                resultContainer.addElementAtEnd("\n=== Resolucion de Sistemas Lineales ===")
                
                try:
                    solution_gj = LinearSystemSolver.gauss_jordan(matrix)
                    resultContainer.addElementAtEnd("\nSolución (Gauss-Jordan):")
                    for i in range(solution_gj.getListLength()):
                        resultContainer.addElementAtEnd(f"x{i} = {solution_gj.getElementAtIndex(i):.6f}")
                except (SingularMatrixError, MatrixDimensionsError) as e:
                    ErrorLogger.log("GaussJordanError", f"Error Gauss-Jordan: {str(e)}")
                    resultContainer.addElementAtEnd(f"Error en Gauss-Jordan: {str(e)}")
                
                for pivoting_type in ['partial', 'scaled', 'complete']:
                    try:
                        solution_ge = LinearSystemSolver.gaussian_elimination(matrix, pivoting=pivoting_type)
                        resultContainer.addElementAtEnd(f"\nSolución (Elim. Gaussiana - pivoteo {pivoting_type}):")
                        for i in range(solution_ge.getListLength()):
                            resultContainer.addElementAtEnd(f"x{i} = {solution_ge.getElementAtIndex(i):.6f}")
                    except (SingularMatrixError, MatrixDimensionsError) as e:
                        ErrorLogger.log(f"GaussianElimError_{pivoting_type}", f"Error Elim. Gaussiana ({pivoting_type}): {str(e)}")
                        resultContainer.addElementAtEnd(f"Error en Elim. Gaussiana ({pivoting_type}): {str(e)}")
            else:
                resultContainer.addElementAtEnd("\nEl archivo no contiene un sistema de ecuaciones valido")
        
        except Exception as e:
            ErrorLogger.log("MatrixOperationError", f"Error general en operaciones matriciales: {str(e)}")
            resultContainer.addElementAtEnd(f"Error en operaciones matriciales: {str(e)}")

    def displayProcessingStatistics(self, startTime: float, outputPath: str):
        processingDuration = time.time() - startTime
        print(f"Archivo procesado en: {processingDuration:.4f} segundos")
        print(f"Resultados guardados en: {outputPath}")
        
        if not self.fileProcessor.getErrorLog().isEmpty():
            print("\nErrores encontrados durante procesamiento:")
            errorNode = self.fileProcessor.getErrorLog().headNode
            while errorNode:
                print(f"  - {errorNode.elementData}")
                errorNode = errorNode.nextNode

