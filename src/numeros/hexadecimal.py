from numeros.numero import Number
from utilidades.normalizador import normalizeHexadecimal
from errores.tiposErrores import InvalidNumberFormatError

class Hexadecimal(Number):
    def __init__(self, valorEntrada: str):
        """
        Representa un número hexadecimal con validación y análisis.
        
        Args:
            valorEntrada: Cadena hexadecimal (ej: "1A.3F")
            
        Raises:
            InvalidNumberFormatError: Si formato inválido
        """
        valorProcesado = valorEntrada.upper().replace(' ', '')
        super().__init__(valorProcesado)
    
    def determinarBase(self) -> int:
        return 16
    
    def esValido(self, valor: str) -> bool:
        """
        Valida formato hexadecimal (0-9, A-F, punto decimal opcional).
        
        Args:
            valor: Cadena a validar
            
        Returns:
            True si es hexadecimal válido
        """
        if valor.startswith('-') or valor.startswith('+'):
            valor = valor[1:]
        
        partes = valor.split('.')
        if len(partes) > 2:
            return False
        
        caracteresValidos = '0123456789ABCDEF'
        return all(all(c in caracteresValidos for c in parte) for parte in partes if parte)
    
    def normalizar(self):
        self.formaNormalizada = normalizeHexadecimal(self.valorOriginal)
    
    def contarCifrasSignificativas(self):
        """Misma lógica que decimal/binario"""
        valor = self.valorOriginal
        
        if valor.startswith('-') or valor.startswith('+'):
            valor = valor[1:]
        
        if valor.replace('0', '').replace('.', '').replace('A', '').replace('B', '').replace('C', '').replace('D', '').replace('E', '').replace('F', '') == '':
            self.cifrasSignificativas = 1
            return
        
        partes = valor.split('.')
        parteEntera = partes[0].lstrip('0')
        parteDecimal = partes[1].rstrip('0') if len(partes) > 1 else ""
        
        if parteEntera:
            self.cifrasSignificativas = len(parteEntera) + len(parteDecimal)
        else:
            for i, char in enumerate(parteDecimal):
                if char != '0':
                    self.cifrasSignificativas = len(parteDecimal) - i
                    return
            self.cifrasSignificativas = 1
    
    def determinarOperacionesSoportadas(self):
        """Hexadecimales soportan +, -, *, / (excepto división por cero)"""
        self.operacionesSoportadas = ['+', '-', '*']
        
        # Permitir división solo si no es cero
        caracteresNoCero = self.valorOriginal.replace('0', '').replace('.', '').replace('-', '').replace('+', '')
        if caracteresNoCero:
            self.operacionesSoportadas.append('/')
    
    def convertirADecimal(self) -> float:
        """Convierte hexadecimal a valor decimal"""
        signo = -1 if self.valorOriginal.startswith('-') else 1
        valor = self.valorOriginal.replace('-', '').replace('+', '')
        
        partes = valor.split('.')
        entero = int(partes[0], 16) if partes[0] else 0
        decimal = 0.0
        
        if len(partes) > 1 and partes[1]:
            for i, char in enumerate(partes[1], 1):
                decimal += int(char, 16) * (16 ** (-i))
        
        return signo * (entero + decimal)
    
    # Métodos de acceso (mismos que Decimal/Binario)