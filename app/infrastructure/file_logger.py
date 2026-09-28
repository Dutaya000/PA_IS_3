import datetime
from app.core.interfaces import ILogger

class FileLogger(ILogger):
    def __init__(self, file_path: str = "notifications.log"):
        # Invariante: El path del archivo de logs debe ser válido
        if not file_path:
            raise ValueError("Invariante violada: Ruta de log inválida.")
        self.file_path = file_path

    def log(self, message: str) -> None:
        # Precondición
        if not message or not message.strip():
            raise ValueError("Precondición fallida: El mensaje de log no puede estar vacío.")
        
        timestamp = datetime.datetime.now().isoformat()
        log_entry = f"[{timestamp}] {message}\n"
        
        # Postcondición: Escritura persistente garantizada
        with open(self.file_path, "a", encoding="utf-8") as f:
            f.write(log_entry)

