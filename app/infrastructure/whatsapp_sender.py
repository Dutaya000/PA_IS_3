from app.core.interfaces import INotificationSender

class WhatsAppSender(INotificationSender):
    async def send(self, destination: str, message: str) -> bool:
        if not destination or not message:
            return False
        print(f"[WhatsApp Business API] Enviando mensaje a {destination}: '{message}'")
        return True
