from app.core.interfaces import INotificationSender

class SMSSender(INotificationSender):
    async def send(self, destination: str, message: str) -> bool:
        # SRP: Lógica exclusiva para conectarse a pasarelas SMS (ej. Twilio)
        if not destination or not message:
            return False
        print(f"[SMS Gateway] Enviando SMS a {destination}: {message}")
        return True
