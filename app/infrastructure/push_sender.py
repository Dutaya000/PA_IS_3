from app.core.interfaces import INotificationSender

class PushSender(INotificationSender):
    async def send(self, destination: str, message: str) -> bool:
        if not destination or not message:
            return False
        print(f"[Push Service] Enviando notificación push al DeviceID {destination}: '{message}'")
        return True
