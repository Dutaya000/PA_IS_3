import pytest
import os
from app.infrastructure.email_sender import EmailSender
from app.infrastructure.sms_sender import SMSSender
from app.infrastructure.push_sender import PushSender
from app.infrastructure.whatsapp_sender import WhatsAppSender
from app.infrastructure.file_logger import FileLogger
from app.services.notification_service import NotificationManager

# --- 5.2.1 PRUEBAS PARA CANALES INDIVIDUALES ---

@pytest.mark.anyio
async def test_email_sender_success():
    sender = EmailSender()
    result = await sender.send("test@techsolutions.com", "Mensaje de prueba")
    assert result is True

@pytest.mark.anyio
async def test_sms_sender_success():
    sender = SMSSender()
    result = await sender.send("+51999999999", "Mensaje SMS")
    assert result is True

@pytest.mark.anyio
async def test_push_sender_success():
    sender = PushSender()
    result = await sender.send("device_token_123", "Mensaje Push")
    assert result is True

@pytest.mark.anyio
async def test_whatsapp_sender_success():
    sender = WhatsAppSender()
    result = await sender.send("+51999999999", "Mensaje WhatsApp")
    assert result is True


# --- 5.2.2 PRUEBAS PARA SISTEMA DE LOGGING Y CONTRATOS ---

def test_file_logger_and_invariants():
    test_log_path = "test_run.log"
    
    # Prueba de Invariante: Ruta vacía debe lanzar ValueError
    with pytest.raises(ValueError, match="Invariante violada"):
        FileLogger(file_path="")
        
    logger = FileLogger(file_path=test_log_path)
    
    # Prueba de Precondición: Mensaje vacío debe lanzar ValueError
    with pytest.raises(ValueError, match="Precondición fallida"):
        logger.log("")
        
    # Registro válido
    logger.log("Log de prueba unitaria")
    
    assert os.path.exists(test_log_path)
    with open(test_log_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "Log de prueba unitaria" in content
        
    # Limpieza del archivo temporal de pruebas
    os.remove(test_log_path)


# --- 5.2.3 PRUEBAS PARA NOTIFICATIONMANAGER (MULTI-CANAL Y ERRORES) ---

@pytest.mark.anyio
async def test_notification_manager_multichannel_success():
    test_log = "test_manager.log"
    logger = FileLogger(file_path=test_log)
    manager = NotificationManager(logger=logger)
    
    # Inyección de dependencias y registro de canales (OCP)
    manager.register_channel("email", EmailSender())
    manager.register_channel("sms", SMSSender())
    
    destinations = {
        "email": "user@techsolutions.com",
        "sms": "+51987654321"
    }
    
    # Envío simultáneo
    report = await manager.send_multichannel(destinations, "Alerta de sistema")
    
    assert report["email"] == "Enviado con éxito"
    assert report["sms"] == "Enviado con éxito"
    assert os.path.exists(test_log)
    os.remove(test_log)

@pytest.mark.anyio
async def test_notification_manager_preconditions():
    logger = FileLogger(file_path="test_rules.log")
    manager = NotificationManager(logger=logger)
    
    # Precondición: Mensaje vacío debe lanzar error
    with pytest.raises(ValueError, match="Precondición fallida"):
        await manager.send_multichannel({"email": "test@test.com"}, "")
        
    # Precondición: Destinos vacíos debe lanzar error
    with pytest.raises(ValueError, match="Precondición fallida"):
        await manager.send_multichannel({}, "Hola")

@pytest.mark.anyio
async def test_notification_manager_isolated_errors():
    """
    Simula una falla crítica en un canal para verificar que no afecte a los demás.
    """
    class BrokenChannel:
        async def send(self, destination, message):
            raise RuntimeError("Conexión perdida con la pasarela")
            
    test_log = "test_isolated.log"
    logger = FileLogger(file_path=test_log)
    manager = NotificationManager(logger=logger)
    
    # Registramos un canal funcional y uno defectuoso
    manager.register_channel("email", EmailSender())
    manager.register_channel("whatsapp", BrokenChannel()) # Canal roto
    
    destinations = {
        "email": "ok@techsolutions.com",
        "whatsapp": "+510000000"
    }
    
    report = await manager.send_multichannel(destinations, "Mensaje crítico corporativo")
    
    # Aislamiento verificado: El canal email fue exitoso a pesar de la caída de WhatsApp
    assert report["email"] == "Enviado con éxito"
    assert "Error Crítico" in report["whatsapp"]
    
    if os.path.exists(test_log):
        os.remove(test_log)
