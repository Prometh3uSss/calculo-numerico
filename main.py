import os
import time
from src.archivos.lectorArchivos import FileReader  # Cambiado a FileReader
from src.utilidades.Generador import FileGenerator  # Asumiendo nuevo nombre
from src.estructuras.listaEnlazada import LinkedList
from src.errores.tiposErrores import InvalidNumberFormatError, FileNameError
from src.errores.calculadoraErrores import ErrorCalculator

def main():
    # Configurar rutas
    dataFolderPath = os.path.join(os.getcwd(), 'data')
    outputFolderPath = os.path.join(os.getcwd(), 'salida')
    
    # Crear carpeta de salida si no existe
    if not os.path.exists(outputFolderPath):
        os.makedirs(outputFolderPath)
    
    # Inicializar componentes
    fileReader = FileReader()
    fileGenerator = FileGenerator(outputFolderPath)  # Asumiendo nuevo nombre
    
    # Obtener lista de archivos a procesar
    filesToProcess = getDataFiles(dataFolderPath)
    
    if not filesToProcess:
        print("No se encontraron archivos válidos para procesar en la carpeta 'data'")
        return
    
    # Procesar cada archivo
    for filePath in filesToProcess:
        processFile(filePath, fileReader, fileGenerator)

def getDataFiles(folderPath: str) -> list:
    """Obtiene la lista de archivos .txt en la carpeta data"""
    fileList = []
    try:
        for fileName in os.listdir(folderPath):
            if fileName.endswith('.txt'):
                fullPath = os.path.join(folderPath, fileName)
                fileList.append(fullPath)
    except FileNotFoundError:
        print(f"Advertencia: La carpeta 'data' no existe en {folderPath}")
    return fileList

def processFile(filePath: str, fileReader: FileReader, fileGenerator: FileGenerator):
    """Procesa un archivo completo y genera los resultados"""
    fileName = os.path.basename(filePath)
    print(f"\n{'='*50}")
    print(f"Procesando archivo: {fileName}")
    print(f"{'='*50}")
    
    try:
        startTime = time.time()
        
        # Paso 1: Leer y procesar el archivo
        dataList = fileReader.processFile(filePath)
        rows, columns = fileReader.getDimensions()  # Asumiendo nuevo nombre
        print(f"Archivo procesado: {rows} filas x {columns} columnas")
        
        # Paso 2: Calcular resultados para cada número
        resultsList = LinkedList()
        processData(dataList, resultsList)
        
        # Paso 3: Calcular errores (si hay suficientes datos)
        calculateErrors(dataList, resultsList)
        
        # Paso 4: Generar archivo de salida
        baseName = fileName.split('_')[0]
        outputPath = fileGenerator.generateOutputFile(baseName, resultsList)  # Asumiendo nuevo nombre
        
        # Paso 5: Mostrar estadísticas
        elapsedTime = time.time() - startTime
        print(f"Archivo procesado en {elapsedTime:.4f} segundos")
        print(f"Resultados guardados en: {outputPath}")
        
        # Mostrar errores si los hay
        if fileReader.errorList.length > 0:
            print("\nErrores encontrados durante el procesamiento:")
            currentError = fileReader.errorList.head
            while currentError:
                print(f"  - {currentError.data}")
                currentError = currentError.next
        
    except (FileNotFoundError, IOError) as e:
        print(f"Error de E/S: {str(e)}")
    except FileNameError as e:
        print(f"Error en nombre de archivo: {str(e)}")
    except InvalidNumberFormatError as e:
        print(f"Error en formato numérico: {str(e)}")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")

def processData(dataList: LinkedList, resultsList: LinkedList):
    """Procesa los datos y genera resultados para cada número"""
    currentRowNode = dataList.head
    currentRowNumber = 1
    
    while currentRowNode:
        # Procesar cada número en la fila
        currentNumberNode = currentRowNode.data.head
        currentColumnNumber = 1
        
        while currentNumberNode:
            # Obtener el objeto numérico
            numberObject = currentNumberNode.data
            
            # Crear cadena de resultado
            resultString = (
                f"Fila {currentRowNumber}, Col {currentColumnNumber}: "
                f"Valor: {numberObject.originalValue} | "
                f"Sistema: {numberObject.getNumberSystem()} | "
                f"Normalizado: {numberObject.getNormalizedValue()} | "
                f"Cifras Signif: {numberObject.countSignificantDigits()} | "
                f"Operaciones: {numberObject.getPossibleOperations()}"
            )
            
            resultsList.append(resultString)
            
            currentNumberNode = currentNumberNode.next
            currentColumnNumber += 1
        
        currentRowNode = currentRowNode.next
        currentRowNumber += 1

def calculateErrors(dataList: LinkedList, resultsList: LinkedList):
    """Calcula errores para los números procesados (si es posible)"""
    # Solo calculamos errores si hay al menos 2 números
    if dataList.length < 2:
        return
    
    # Obtener los primeros dos números para comparación
    firstNumber = dataList.head.data.head.data
    secondNumber = dataList.head.data.head.next.data if dataList.head.data.head.next else None
    
    if not secondNumber:
        return
    
    try:
        # Convertir a valores decimales para cálculo de errores
        exactValue = firstNumber.toDecimal()
        approximateValue = secondNumber.toDecimal()
        
        # Calcular errores
        absoluteError = ErrorCalculator.absoluteError(exactValue, approximateValue)
        relativeError = ErrorCalculator.relativeError(exactValue, approximateValue)
        
        # Agregar resultados de errores
        resultsList.append("\n=== Resultados de Análisis de Errores ===")
        resultsList.append(f"Comparación: {firstNumber.originalValue} vs {secondNumber.originalValue}")
        resultsList.append(f"Error Absoluto: {absoluteError}")
        resultsList.append(f"Error Relativo: {relativeError}")
        
        # Calcular errores de redondeo y truncamiento para el primer número
        significantDigits = firstNumber.countSignificantDigits()
        roundingError = ErrorCalculator.roundingError(exactValue, significantDigits)
        truncationError = ErrorCalculator.truncationError(exactValue, significantDigits)
        
        resultsList.append(f"Error por Redondeo ({firstNumber.originalValue}): {roundingError}")
        resultsList.append(f"Error por Truncamiento ({firstNumber.originalValue}): {truncationError}")
        
    except Exception as e:
        resultsList.append(f"Error al calcular errores: {str(e)}")

if __name__ == "__main__":
    main()