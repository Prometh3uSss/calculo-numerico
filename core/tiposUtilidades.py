classRegistry = {}

def registerType(typeName, typeClass):
    classRegistry[typeName] = typeClass

def isTypeInstance(objectInstance, typeName):
    if typeName not in classRegistry:
        return False
    
    targetClass = classRegistry[typeName]
    currentClass = type(objectInstance)
    
    while currentClass is not None:
        if currentClass == targetClass:
            return True
        currentClass = currentClass.__base__
    
    return False

def allElementsMeet(iterable, conditionFunction):
    for element in iterable:
        if not conditionFunction(element):
            return False
    return True