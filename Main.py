from LeerArch import FileHandler
from SistemaNumerico import Numero
from Generador import generar_archivo_salida


def main():
     handler = FileHandler("mis_datos.bin")
     datos = handler.get_datos()
     filas, columnas = handler.get_dimensiones()

     resultados = []
     for i in range(filas):
         for j in range(columnas):
             valor_str = datos.obtener_elemento(i, j)
             if valor_str:
                 num = Numero(valor_str)
                 resultados.append(num.resultado_completo())

     nombre_archivo = generar_archivo_salida(resultados)
     print(f"Archivo generado: {nombre_archivo}")

if __name__ == "__main__":
     main()