from numeros.numero import Number
from utilidades.normalizador import normalizeBinary
from errores.tiposErrores import InvalidNumberFormatError

class Binario(Number):
    def __init__(self, valorEntrada: str):
        """
        Representa un número binario con validación y análisis.
        
        Args:
            valorEntrada: Cadena binaria (ej: "101.01")
            
        Raises:
            InvalidNumberFormatError: Si formato inválido
        """
        valorProcesado = valorEntrada.replace(' ', '')
        super().__init__(valorProcesado)
    
    def determinarBase(self) -> int:
        return 2
    
    def esValido(self, valor: str) -> bool:
        """
        Valida formato binario (0-1, punto decimal opcional).
        
        Args:
            valor: Cadena a validar
            
        Returns:
            True si es binario válido
        """
        # Manejar signo
        if valor.startswith('-') or valor.startswith('+'):
            valor = valor[1:]
        
        partes = valor.split('.')
        if len(partes) > 2:
            return False
        
        return all(all(c in '01' for c in parte) for parte in partes if parte)
    
    def normalizar(self):
        self.formaNormalizada = normalizeBinary(self.valorOriginal)
    
    def contarCifrasSignificativas(self):
        """Misma lógica que decimal pero para binario"""
        valor = self.valorOriginal
        
        if valor.startswith('-') or valor.startswith('+'):
            valor = valor[1:]
        
        if valor.replace('0', '').replace('.', '') == '':
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
        """Binarios soportan +, -, *, / (excepto división por cero)"""
        self.operacionesSoportadas = ['+', '-', '*']
        
        # Permitir división solo si no es cero
        if not all(c in '0.' for c in self.valorOriginal.replace('-', '').replace('+', '')):
            self.operacionesSoportadas.append('/')
    
    def convertirADecimal(self) -> float:
        """Convierte binario a valor decimal"""
        signo = -1 if self.valorOriginal.startswith('-') else 1
        valor = self.valorOriginal.replace('-', '').replace('+', '')
        
        partes = valor.split('.')
        entero = int(partes[0], 2) if partes[0] else 0
        decimal = 0.0
        
        if len(partes) > 1 and partes[1]:
            for i, bit in enumerate(partes[1], 1):
                if bit == '1':
                    decimal += 2 ** (-i)
        
        return signo * (entero + decimal)
    
    # Métodos de acceso (mismos que Decimal)