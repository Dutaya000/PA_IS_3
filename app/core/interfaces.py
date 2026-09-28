from abc import ABC, abstractmethod

class INotificationSender(ABC):
    """
    Abstracción formal para los canales de envío (Cumple con DIP y OCP).
    Cualquier canal nuevo debe implementar obligatoriamente esta interfaz.
    """
    @abstractmethod
    async def send(self, destination: str, message: str) -> bool:
        """
        Contrato de envío de notificaciones.
        Precondición: destination y message no vacíos.
        Postcondición: Retorna True si fue exitoso, False si falló.
        """
        pass


class ILogger(ABC):
    """
    Abstracción formal para el mecanismo de logging (Cumple con DIP).
    Permite registrar las operaciones sin acoplar el sistema a un archivo o base de datos específica.
    """
    @abstractmethod
    def log(self, message: str) -> None:
        """
        Contrato para el registro de eventos.
        Precondición: message no nulo ni vacío.
        Postcondición: El mensaje queda escrito en el destino persistente configurado.
        """
        pass
