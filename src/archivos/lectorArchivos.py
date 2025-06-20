
from estructuras.listaEnlazada import ListaEnlazada
from numeros.binario import Binario
from numeros.decimal import Decimal
from numeros.hexadecimal import Hexadecimal
from validadorFormato import ValidadorFormato
from errores.tiposErrores import FormatoNumeroInvalidoError, NombreArchivoError

class lectorArchivos:
    def _init_(self):
        self.datos = ListaEnlazada()
    
    def procesarArchivo(self, ruta):
        nombreArchivo = ruta.split('/')[-1]
        
        if not ValidadorFormato.validarNombreArchivo(nombreArchivo):
            raise NombreArchivoError(f"Formato de nombre invalido: {nombreArchivo}")
        
        try:
            with open(ruta, 'r') as f:
                lineas = f.readlines()
        except FileNotFoundError:
            raise FileNotFoundError(f"Archivo no encontrado: {ruta}")
        
        for i, linea in enumerate(lineas):
            fila = ListaEnlazada()
            datosLinea = linea.strip().split('#')
            
            for dato in datosLinea:
                if not dato:
                    continue
                
                try:
                    
                    if '.' in dato or ',' in dato:
                        fila.agregar(Decimal(dato))
                    elif all(c in '01.' for c in dato):
                        fila.agregar(Binario(dato))
                    elif all(c in '0123456789abcdefABCDEF.' for c in dato):
                        fila.agregar(Hexadecimal(dato))
                    else:
                        raise FormatoNumeroInvalidoError(f"Formato no reconocido: {dato}")
                except FormatoNumeroInvalidoError as e:
                    print(f"Error en linea {i+1}, dato '{dato}': {str(e)}")
            
            if len(fila) > 0:
                self.datos.agregar(fila)
        
        return self.datos