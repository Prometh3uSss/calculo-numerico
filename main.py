import os
from src.utilidades.LeerArch import LectorArchivosBin
from src.numeros.CalculosNumericos import Numero
from src.utilidades.Generador import GeneradorArchivos

def main():
    rutaCarpetaArchivosBin = os.path.join('src', 'archivos')
    
    rutaCarpetaSalida = os.path.join('src', 'ArchivosDeSalida') 

    
    os.makedirs(rutaCarpetaSalida, existOk=True) 

    lector = LectorArchivosBin(rutaCarpetaArchivosBin)
    archivosParaProcesar = lector.obtenerArchivosParaProcesar()

    generador = GeneradorArchivos(rutaCarpetaSalida)

    if not archivosParaProcesar:
        print("No hay archivos .bin validos para procesar")
        return

    for nombreArchivoBin, matrizDatos in archivosParaProcesar:
        print(f"Procesando datos de: {nombreArchivoBin}")
        
        resultadosParaTxt = []
        filas, columnas = matrizDatos.dimensiones()

        for r in range(filas):
            for c in range(columnas):
                valorOriginal = matrizDatos.obtenerElemento(r, c)
                if valorOriginal is None:
                    continue 

                if valorOriginal.startswith("Ocho:"):
                    resultadosParaTxt.append(f"{valorOriginal} | Excluido (Octal)")
                elif valorOriginal.startswith("z%:"):
                    resultadosParaTxt.append(f"{valorOriginal} | No reconocido")
                else:
                    try:
                        num = Numero(valorOriginal)
                        resultadosParaTxt.append(num.resultadoCompleto())
                    except Exception as e:
                        resultadosParaTxt.append(f"{valorOriginal} | Error al procesar: {e}")

        nombreBaseOriginal = os.path.splitext(nombreArchivoBin)[0].split('_')[0]

        nombreArchivoGenerado = generador.generarArchivoSalida(nombreBaseOriginal, resultadosParaTxt)
        
        if nombreArchivoGenerado:
            print(f"Resultados de '{nombreArchivoBin}' guardados en: {nombreArchivoGenerado}")
        else:
            print(f"No se pudo generar el archivo de salida para '{nombreArchivoBin}'.")

if __name__ == "__main__":
    main()