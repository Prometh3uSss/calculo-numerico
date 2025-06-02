from datetime import datetime
import random

def generar_archivo_salida(resultados: list):
    fecha_actual = datetime.now().strftime("%Y%m%d")
    serial = random.randint(0, 100)
    nombre_archivo = f"{fecha_actual}_{serial}.txt"
    
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            for resultado in resultados:
                archivo.write(resultado + "\n")
        return nombre_archivo
    except Exception as e:
        print(f"Error al generar archivo: {e}")
        return None