class CalculadoraErrores:
    @staticmethod
    def error_absoluto(real, aproximado):
        return abs(real - aproximado)
    
    @staticmethod
    def error_relativo(real, aproximado):
        if real == 0:
            return float('inf') if aproximado != 0 else 0
        return abs(real - aproximado) / abs(real)
    
    @staticmethod
    def error_redondeo(valor, cifras_significativas):
        return 0.5 * 10 ** (-cifras_significativas)
    
    @staticmethod
    def error_truncamiento(valor, cifras_significativas):
        return 10 ** (-cifras_significativas)
    
    @staticmethod
    def error_propagacion_suma(*errores):
        return sum(errores)
    
    @staticmethod
    def error_propagacion_producto(valores, errores):
        total = 0
        for i in range(len(valores)):
            if valores[i] == 0:
                return float('inf')
            total += (errores[i] / abs(valores[i])) ** 2
        return abs(valores[0] * valores[1]) * total ** 0.5