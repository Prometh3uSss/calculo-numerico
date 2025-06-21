from numero import Numero

class Binario(Numero):
    def validar(self):
        if not all(c in '01.' for c in self.valor):
            raise ValueError(f"Valor '{self.valor}' no es binario valido")
        self.sistema = "Binario"
    
    def calcularCifrasSignificativas(self):
        partes = self.valor.split('.')
        if len(partes) == 1:
            self.cifrasSignificativas = len(partes[0].lstrip('0'))
        else:
            self.cifrasSignificativas = len(partes[0].lstrip('0')) + len(partes[1].rstrip('0'))
    
    def aDecimal(self):
        partes = self.valor.split('.')
        entero = int(partes[0], 2) if partes[0] else 0
        decimal = 0
        if len(partes) > 1 and partes[1]:
            decimal = sum(int(bit) * 2**(-i-1) for i, bit in enumerate(partes[1]))
        return entero + decimal
    
    def formaNormalizada(self):
        decimal = self.aDecimal()
        if decimal == 0:
            return "0"
        
        exponente = 0
        num = abs(decimal)
        while num >= 2:
            num /= 2
            exponente += 1
        while num < 1:
            num *= 2
            exponente -= 1
        
        signo = "-" if decimal < 0 else ""
        return f"{signo}{num:.4f} × 2^{exponente}"