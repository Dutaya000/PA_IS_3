from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from app.services.notification_service import NotificationManager
from app.infrastructure.email_sender import EmailSender
from app.infrastructure.sms_sender import SMSSender
from app.infrastructure.push_sender import PushSender
from app.infrastructure.whatsapp_sender import WhatsAppSender
from app.infrastructure.file_logger import FileLogger

# Creamos el enrutador que FastAPI necesita importar
router = APIRouter()

# Instanciamos el logger y el manager inyectando dependencias (DIP)
logger_instance = FileLogger()
manager = NotificationManager(logger=logger_instance)

# Registro dinámico de canales aplicando OCP
manager.register_channel("email", EmailSender())
manager.register_channel("sms", SMSSender())
manager.register_channel("push", PushSender())
manager.register_channel("whatsapp", WhatsAppSender())

class NotificationRequest(BaseModel):
    destinations: dict[str, str] = Field(..., example={"email": "cliente@techsolutions.com"})
    message: str = Field(..., min_length=1, max_length=1000)

@router.post("/notifications/send")
async def send_notification(request: NotificationRequest):
    try:
        report = await manager.send_multichannel(request.destinations, request.message)
        return {"status": "Procesado", "report": report}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
