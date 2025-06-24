from core.tiposUtilidades import registerType
from numeros.decimal import Decimal
from numeros.binario import Binary
from numeros.hexadecimal import Hexadecimal

def initializeTypeSystem():
    registerType("Decimal", Decimal)
    registerType("Binary", Binary)
    registerType("Hexadecimal", Hexadecimal)