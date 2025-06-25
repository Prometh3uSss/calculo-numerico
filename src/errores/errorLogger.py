import os
import random
from datetime import datetime
from estructuras.listaEnlazada import LinkedList
from algebra.matrix import Matrix

class ErrorLogger:
    _log_dir = "log"
    _log_file = os.path.join(_log_dir, "errores.log")
    
    @staticmethod
    def _ensure_log_directory_exists():
        if not os.path.exists(ErrorLogger._log_dir):
            os.makedirs(ErrorLogger._log_dir)

    @staticmethod
    def log(error_type: str, details: str):
        ErrorLogger._ensure_log_directory_exists()
        
        timestamp = datetime.now().strftime("%Y%m%d")
        serial = random.randint(100, 999)
        log_entry = f"{error_type}_{timestamp}_{serial}: {details}\n"
        
        try:
            with open(ErrorLogger._log_file, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except Exception as e:
            print(f"CRITICAL: No se pudo escribir en log: {str(e)}")
            print(f"Log entry: {log_entry}")
    
    @staticmethod
    def log_matrix_operation(matrix: Matrix, operation: str, error: Exception):
        details = f"Operacion: {operation}, Dimensiones: {matrix.rows}x{matrix.cols}, Error: {str(error)}"
        ErrorLogger.log("MatrixOperationError", details)