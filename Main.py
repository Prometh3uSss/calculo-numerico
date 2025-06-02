from LeerArch import FileHandler
from SistemaNumerico import Numero
from Generador import generar_archivo_salida

def main():
    # 1. Leer archivo .bin
    try:
        handler = FileHandler("mis_datos.bin")  # Asegúrate de que la ruta sea correcta
        datos = handler.get_datos()
        filas, columnas = handler.get_dimensiones()
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return

    # 2. Procesar cada valor
    resultados = []
    for i in range(filas):
        for j in range(columnas):
            valor_str = datos.obtener_elemento(i, j)
            if valor_str:
                num = Numero(valor_str)
                if num.es_valido:  # Ahora esta propiedad existe
                    resultados.append(num.resultado_completo())
                else:
                    resultados.append(f"{num.valor_original} | {num.mensaje_error}")

    # 3. Generar archivo de salida
    nombre_archivo = generar_archivo_salida(resultados)
    print(f"Archivo generado: {nombre_archivo}")
main()
