from numeros.numero import Number
from utilidades.normalizador import normalizeDecimal
from errores.tiposErrores import InvalidNumberFormatError

class Decimal(Number):
    def __init__(self, valorEntrada: str):
        """
        Representa un número decimal con validación, normalización y análisis de cifras significativas.
        
        Args:
            valorEntrada: Cadena que representa el número decimal
            
        Raises:
            InvalidNumberFormatError: Si el formato no es válido
        """
        valorProcesado = valorEntrada.replace(',', '.').replace(' ', '')
        super().__init__(valorProcesado)
    
    def determinarBase(self) -> int:
        return 10
    
    def esValido(self, valor: str) -> bool:
        """
        Valida formato decimal (dígitos, signo opcional, punto decimal opcional).
        
        Args:
            valor: Cadena a validar
            
        Returns:
            True si es válido, False en caso contrario
        """
        # Patrón: [signo]dígitos[.dígitos]
        if valor.startswith('-') or valor.startswith('+'):
            valor = valor[1:]
        
        partes = valor.split('.')
        if len(partes) > 2:
            return False  # Múltiples puntos decimales
        
        # Todas las partes deben ser dígitos
        return all(parte.isdigit() for parte in partes if parte)
    
    def normalizar(self):
        """Convierte a notación científica decimal"""
        self.formaNormalizada = normalizeDecimal(self.valorOriginal)
    
    def contarCifrasSignificativas(self):
        """
        Calcula cifras significativas según reglas:
        - Ceros iniciales no significativos
        - Ceros finales después del punto son significativos
        - Ceros entre dígitos significativos
        """
        valor = self.valorOriginal
        
        # Manejar signo
        if valor.startswith('-') or valor.startswith('+'):
            valor = valor[1:]
        
        # Caso especial: cero
        if valor.replace('0', '').replace('.', '') == '':
            self.cifrasSignificativas = 1
            return
        
        partes = valor.split('.')
        parteEntera = partes[0].lstrip('0')
        
        if len(partes) > 1:
            parteDecimal = partes[1].rstrip('0')
        else:
            parteDecimal = ""
        
        if parteEntera:
            self.cifrasSignificativas = len(parteEntera) + len(parteDecimal)
        else:
            # Contar desde primer dígito no cero en decimal
            for i, char in enumerate(parteDecimal):
                if char != '0':
                    self.cifrasSignificativas = len(parteDecimal) - i
                    return
            self.cifrasSignificativas = 1
    
    def determinarOperacionesSoportadas(self):
        """Decimales soportan todas las operaciones básicas"""
        self.operacionesSoportadas = ['+', '-', '*', '/']
    
    def convertirADecimal(self) -> float:
        """Convierte a valor flotante decimal"""
        return float(self.valorOriginal.replace(',', '.'))
    
    def obtenerValorOriginal(self) -> str:
        return self.valorOriginal
    
    def obtenerFormaNormalizada(self) -> str:
        return self.formaNormalizada
    
    def obtenerCantidadCifrasSignificativas(self) -> int:
        return self.cifrasSignificativas
    
    def obtenerOperacionesSoportadas(self) -> list:
        return self.operacionesSoportadas
    
    def obtenerBase(self) -> int:
        return self.base
    
    def __str__(self) -> str:
        return (f"Decimal: {self.valorOriginal} | "
                f"Normalizado: {self.formaNormalizada} | "
                f"Cifras: {self.cifrasSignificativas} | "
                f"Operaciones: {''.join(self.operacionesSoportadas)}")