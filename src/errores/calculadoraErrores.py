class calculadoraErrores:
    @staticmethod
    def errorAbsoluto(valorReal, valorAproximado):
        return abs(valorReal - valorAproximado)
    
    @staticmethod
    def errorRelativo(valorReal, valorAproximado):
        if valorReal == 0:
            return float('inf') if valorAproximado != 0 else 0
        return abs(valorReal - valorAproximado) / abs(valorReal)
    
    @staticmethod
    def errorRedondeo(valorReal, cifrasSignificativas):
        return 0.5 * 10**(-cifrasSignificativas)
    
    @staticmethod
    def errorTruncamiento(valorReal, cifrasSignificativas):
        return 10**(-cifrasSignificativas)
    
    @staticmethod
    def errorPropagacionSuma(errors):
        return sum(errors)
    
    @staticmethod
    def errorPropagacionProducto(valores, errors):
        total = 0
        for i in range(len(valores)):
            termino = errors[i] / abs(valores[i]) if valores[i] != 0 else float('inf')
            total += termino**2
        return abs(valores[0] * valores[1]) * total**0.5