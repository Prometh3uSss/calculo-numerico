import os
from logicaPrincipal import LogicaPrincipal
from errores.errorLogger import ErrorLogger

def main():
    try:
        dataDirectoryPath = os.path.join(os.getcwd(), 'data')
        outputDirectoryPath = os.path.join(os.getcwd(), 'output')
        logsDirectoryPath = os.path.join(os.getcwd(), 'logs')
        
        mainLogic = LogicaPrincipal(dataDirectoryPath, outputDirectoryPath, logsDirectoryPath)
        
        mainLogic.setupProcessingEnvironment()
        
        filesToProcess = mainLogic.getProcessableFiles()
        
        if filesToProcess.getListLength() == 0:
            print("No se encontraron archivos validos para procesar en la carpeta 'data'")
            return
        
        mainLogic.processFileCollection(filesToProcess)
        
    except Exception as criticalError:
        ErrorLogger.log("CriticalSystemError", f"Error critico de ejecucion: {str(criticalError)}")
        print(f"Error critico de ejecucion: {str(criticalError)}")

if __name__ == "__main__":
    main()

