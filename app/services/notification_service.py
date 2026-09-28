import asyncio
from app.core.interfaces import INotificationSender, ILogger

class NotificationManager:
    def __init__(self, logger: ILogger):
        # 1. Uso de Composición: El mánager contiene un diccionario dinámico de canales
        self._channels: dict[str, INotificationSender] = {}
        self._logger = logger

    def register_channel(self, name: str, channel: INotificationSender):
        """Permite registrar nuevos canales dinámicamente en tiempo de ejecución (OCP)."""
        self._channels[name.lower()] = channel

    async def send_multichannel(self, destinations: dict[str, str], message: str) -> dict[str, str]:
        if not message or not destinations:
            raise ValueError("Precondición fallida: Mensaje o destinatarios vacíos.")

        tasks = []
        channel_names = []

        # 2. Implementar envío simultáneo por múltiples canales (Asíncrono/Concurrente)
        for name, dest in destinations.items():
            name_lower = name.lower()
            if name_lower in self._channels:
                channel_names.append(name_lower)
                # Creamos la tarea asíncrona aislada para ejecución en paralelo
                tasks.append(self._execute_channel_send(name_lower, dest, message))

        # Reúne las ejecuciones simultáneas de manera paralela
        results = await asyncio.gather(*tasks)

        # Reconstruye el reporte consolidado final para el cliente
        report = {}
        for res in results:
            report.update(res)

        return report

    async def _execute_channel_send(self, name: str, dest: str, message: str) -> dict[str, str]:
        """
        3. Gestión aislada de errores (try-catch independiente por canal)
        """
        try:
            # Intento de envío a través de la pasarela concreta
            success = await self._channels[name].send(dest, message)
            
            if success:
                status = "Enviado con éxito"
            else:
                status = "Falla técnica en pasarela"
                
        except Exception as e:
            # Captura y aislamiento de cualquier error crítico (Red, Timeout, etc.)
            status = f"Error Crítico: {str(e)}"
            
        # Postcondición obligatoria: Registrar log independientemente del resultado
        self._logger.log(f"Canal: {name} | Destino: {dest} | Resultado: {status}")
        
        return {name: status}

