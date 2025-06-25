from estructuras.listaEnlazada import LinkedList
from errores.tiposErrores import MatrixDimensionsError, SingularMatrixError

class Matrix:
    def __init__(self, rows: int, cols: int, data: LinkedList = None):
        self.rows = rows
        self.cols = cols
        
        if data is None:
            self.data = LinkedList()
            for _ in range(rows):
                row = LinkedList()
                for _ in range(cols):
                    row.addElementAtEnd(0.0)
                self.data.addElementAtEnd(row)
        else:
            self.data = data
    
    def get(self, i: int, j: int) -> float:
        row = self.data.getElementAtIndex(i)
        return row.getElementAtIndex(j)
    
    def set(self, i: int, j: int, value: float):
        row = self.data.getElementAtIndex(i)
        row.setElementAtIndex(j, value)
    
    def swap_rows(self, i: int, j: int):
        row_i = self.data.getElementAtIndex(i)
        row_j = self.data.getElementAtIndex(j)
        self.data.setElementAtIndex(i, row_j)
        self.data.setElementAtIndex(j, row_i)
    
    def scale_row(self, i: int, scalar: float):
        row = self.data.getElementAtIndex(i)
        current = row.headNode
        while current:
            current.elementData *= scalar
            current = current.nextNode
    
    def add_row(self, source_idx: int, target_idx: int, scalar: float = 1.0):
        source = self.data.getElementAtIndex(source_idx)
        target = self.data.getElementAtIndex(target_idx)
        
        source_node = source.headNode
        target_node = target.headNode
        
        while source_node and target_node:
            target_node.elementData += scalar * source_node.elementData
            source_node = source_node.nextNode
            target_node = target_node.nextNode
    
    def is_square(self) -> bool:
        return self.rows == self.cols
    
    def to_augmented(self, constants: LinkedList) -> 'Matrix':
        if constants.getListLength() != self.rows:
            raise MatrixDimensionsError("Número de constantes no coincide con filas")
    
    def add(self, other: 'Matrix') -> 'Matrix':
        if self.rows != other.rows or self.cols != other.cols:
            raise MatrixDimensionsError(
                f"Dimensiones incompatibles para suma: "
                f"{self.rows}x{self.cols} vs {other.rows}x{other.cols}"
            )
    
    def multiply(self, other: 'Matrix') -> 'Matrix':
        if self.cols != other.rows:
            raise MatrixDimensionsError(
                f"Dimensiones incompatibles para multiplicación: "
                f"{self.rows}x{self.cols} vs {other.rows}x{other.cols}"
            )
    
    def __str__(self):
        output = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(f"{self.get(i, j):.4f}")
            output.append(" ".join(row))
        return "\n".join(output)