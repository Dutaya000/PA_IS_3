from app.core.interfaces import INotificationSender

class EmailSender(INotificationSender):
    async def send(self, destination: str, message: str) -> bool:
        # Precondición básica integrada
        if not destination or not message:
            return False
        print(f"[Email API] Enviando correo a {destination}: '{message}'")
        return True