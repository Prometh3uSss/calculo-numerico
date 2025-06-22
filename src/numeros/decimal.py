from .numero import Numero
from ..utilidades.normalizador import normalizar_decimal

class Decimal(Numero):
    def __init__(self, valor: str):
        # Preprocesar valor (reemplazar comas por puntos)
        valor = self._normalizar_formato(valor)
        super().__init__(valor)
        self.base = 10
        self.normalizar()
        self.contar_cifras_significativas()
        self.determinar_operaciones()
    
    def _normalizar_formato(self, valor: str) -> str:
        """Convierte comas en puntos y elimina espacios"""
        return valor.replace(',', '.').replace(' ', '')
    
    def normalizar(self):
        """Convierte el número a notación científica"""
        self.valor_normalizado = normalizar_decimal(self.valor_original)
    
    def contar_cifras_significativas(self):
        """Calcula la cantidad de cifras significativas según reglas matemáticas"""
        valor = self.valor_original
        
        # Manejar signo
        if valor.startswith('-') or valor.startswith('+'):
            valor = valor[1:]
        
        # Caso especial: cero
        if all(c == '0' for c in valor.replace('.', '')):
            self.cifras_significativas = 1
            return
        
        # Dividir en parte entera y decimal
        partes = valor.split('.')
        parte_entera = partes[0].lstrip('0')
        
        if len(partes) > 1:
            parte_decimal = partes[1].rstrip('0')
        else:
            parte_decimal = ""
        
        # Contar cifras significativas
        if parte_entera:
            self.cifras_significativas = len(parte_entera) + len(parte_decimal)
        else:
            # Buscar primer dígito no cero en decimal
            for i, char in enumerate(parte_decimal):
                if char != '0':
                    self.cifras_significativas = len(parte_decimal) - i
                    return
            self.cifras_significativas = 1
    
    def determinar_operaciones(self):
        """Todas las operaciones son posibles para números decimales"""
        self.operaciones_posibles = ['+', '-', '*', '/']
    
    def __str__(self):
        return (f"{self.valor_original} | Base: {self.base} | "
                f"Normalizado: {self.valor_normalizado} | "
                f"Cifras: {self.cifras_significativas} | "
                f"Operaciones: {''.join(self.operaciones_posibles)}")