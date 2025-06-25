from algebra.matrix import Matrix
from errores.tiposErrores import MatrixDimensionsError, SingularMatrixError
from estructuras.listaEnlazada import LinkedList
import math

class LinearSystemSolver:
    @staticmethod
    def gauss_jordan(aug_matrix: Matrix) -> LinkedList:
        if aug_matrix.cols != aug_matrix.rows + 1:
            raise MatrixDimensionsError("Matriz aumentada debe tener n x (n+1)")
        
        n = aug_matrix.rows
        
        for pivot in range(n):
            max_row = pivot
            max_val = abs(aug_matrix.get(pivot, pivot))
            for row in range(pivot + 1, n):
                if abs(aug_matrix.get(row, pivot)) > max_val:
                    max_val = abs(aug_matrix.get(row, pivot))
                    max_row = row
            
            if max_val < 1e-10:
                raise SingularMatrixError("Matriz singular o mal condicionada")
            
            if max_row != pivot:
                aug_matrix.swap_rows(pivot, max_row)
            
            pivot_val = aug_matrix.get(pivot, pivot)
            aug_matrix.scale_row(pivot, 1.0 / pivot_val)
            
            for row in range(n):
                if row != pivot:
                    factor = aug_matrix.get(row, pivot)
                    aug_matrix.add_row(pivot, row, -factor)
        
        solution = LinkedList()
        for i in range(n):
            solution.addElementAtEnd(aug_matrix.get(i, n))
        return solution

    @staticmethod
    def gaussian_elimination(aug_matrix: Matrix, pivoting: str = 'partial') -> LinkedList:
        n = aug_matrix.rows
        
        for pivot in range(n):
            if pivoting == 'partial':
                LinearSystemSolver.partial_pivoting(aug_matrix, pivot)
            elif pivoting == 'scaled':
                LinearSystemSolver.scaled_pivoting(aug_matrix, pivot)
            elif pivoting == 'complete':
                LinearSystemSolver.complete_pivoting(aug_matrix, pivot)
            
            pivot_val = aug_matrix.get(pivot, pivot)
            if abs(pivot_val) < 1e-10:
                raise SingularMatrixError("Matriz singular o mal condicionada")
            
            for row in range(pivot + 1, n):
                factor = aug_matrix.get(row, pivot) / pivot_val
                aug_matrix.add_row(pivot, row, -factor)
        
        solution = LinkedList()
        for i in range(n-1, -1, -1):
            total = aug_matrix.get(i, n)
            for j in range(i+1, n):
                total -= aug_matrix.get(i, j) * solution.getElementAtIndex(j)
            solution.addElementAtBeginning(total / aug_matrix.get(i, i))
        
        return solution

    @staticmethod
    def partial_pivoting(matrix: Matrix, pivot: int):
        max_row = pivot
        max_val = abs(matrix.get(pivot, pivot))
        for row in range(pivot + 1, matrix.rows):
            if abs(matrix.get(row, pivot)) > max_val:
                max_val = abs(matrix.get(row, pivot))
                max_row = row
        if max_row != pivot:
            matrix.swap_rows(pivot, max_row)

    @staticmethod
    def scaled_pivoting(matrix: Matrix, pivot: int):
        scale_factors = []
        for i in range(matrix.rows):
            max_in_row = max(abs(matrix.get(i, j)) for j in range(matrix.cols))
            scale_factors.append(max_in_row if max_in_row > 0 else 1.0)
        
        max_ratio = -1
        max_row = pivot
        for row in range(pivot, matrix.rows):
            ratio = abs(matrix.get(row, pivot)) / scale_factors[row]
            if ratio > max_ratio:
                max_ratio = ratio
                max_row = row
        
        if max_row != pivot:
            matrix.swap_rows(pivot, max_row)

    @staticmethod
    def complete_pivoting(matrix: Matrix, pivot: int):
        max_val = 0
        max_row = pivot
        max_col = pivot
        
        for i in range(pivot, matrix.rows):
            for j in range(pivot, matrix.cols - 1):  
                if abs(matrix.get(i, j)) > max_val:
                    max_val = abs(matrix.get(i, j))
                    max_row = i
                    max_col = j
        
        if max_row != pivot:
            matrix.swap_rows(pivot, max_row)
