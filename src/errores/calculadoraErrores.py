class calculadoraErrores:
    @staticmethod
    def error_absoluto(valor_real, valor_aproximado):
        return abs(valor_real - valor_aproximado)
    
    @staticmethod
    def error_relativo(valor_real, valor_aproximado):
        if valor_real == 0:
            return float('inf') if valor_aproximado != 0 else 0
        return abs(valor_real - valor_aproximado) / abs(valor_real)
    
    @staticmethod
    def error_redondeo(valor_real, cifras_significativas):
        return 0.5 * 10**(-cifras_significativas)
    
    @staticmethod
    def error_truncamiento(valor_real, cifras_significativas):
        return 10**(-cifras_significativas)
    
    @staticmethod
    def error_propagacion_suma(errors):
        return sum(errors)
    
    @staticmethod
    def error_propagacion_producto(valores, errors):
        total = 0
        for i in range(len(valores)):
            termino = errors[i] / abs(valores[i]) if valores[i] != 0 else float('inf')
            total += termino**2
        return abs(valores[0] * valores[1]) * total**0.5