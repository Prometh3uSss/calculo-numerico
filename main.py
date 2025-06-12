import os
from src.utilidades.LeerArch import LectorArchivosBin
from src.numeros.CalculosNumericos import Numero
from src.utilidades.Generador import GeneradorArchivos

def main():
    ruta_carpeta_archivos_bin = os.path.join('src', 'archivos')
    # Modifica la ruta de salida para que apunte a 'ArchivosDeSalida'
    ruta_carpeta_salida = os.path.join('src', 'ArchivosDeSalida') 

    # Asegura que la carpeta de salida exista antes de pasarla a GeneradorArchivos
    os.makedirs(ruta_carpeta_salida, exist_ok=True) 

    lector = LectorArchivosBin(ruta_carpeta_archivos_bin)
    archivos_para_procesar = lector.obtener_archivos_para_procesar()

    generador = GeneradorArchivos(ruta_carpeta_salida)

    if not archivos_para_procesar:
        print("No hay archivos .bin válidos para procesar.")
        return

    for nombre_archivo_bin, matriz_datos in archivos_para_procesar:
        print(f"Procesando datos de: {nombre_archivo_bin}")
        
        resultados_para_txt = []
        filas, columnas = matriz_datos.dimensiones()

        for r in range(filas):
            for c in range(columnas):
                valor_original = matriz_datos.obtener_elemento(r, c)
                if valor_original is None:
                    continue 

                if valor_original.startswith("Ocho:"):
                    resultados_para_txt.append(f"{valor_original} | Excluido (Octal)")
                elif valor_original.startswith("z%:"):
                    resultados_para_txt.append(f"{valor_original} | No reconocido")
                else:
                    try:
                        num = Numero(valor_original)
                        resultados_para_txt.append(num.resultado_completo())
                    except Exception as e:
                        resultados_para_txt.append(f"{valor_original} | Error al procesar: {e}")

        nombre_base_original = os.path.splitext(nombre_archivo_bin)[0].split('_')[0]

        nombre_archivo_generado = generador.generar_archivo_salida(nombre_base_original, resultados_para_txt)
        
        if nombre_archivo_generado:
            print(f"Resultados de '{nombre_archivo_bin}' guardados en: {nombre_archivo_generado}")
        else:
            print(f"No se pudo generar el archivo de salida para '{nombre_archivo_bin}'.")

if __name__ == "__main__":
    main()