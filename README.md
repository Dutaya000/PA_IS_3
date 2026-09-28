# Componente de Gestión de Notificaciones - TechSolutions

Este componente es un motor centralizado de mensajería estructurado bajo **principios de diseño de software robustos**, permitiendo la comunicación multicanal asíncrona, el aislamiento completo de fallas y un acoplamiento extremadamente bajo.

---

## 📝 Introducción y Contextualización

En el ecosistema de **TechSolutions**, la comunicación oportuna y confiable con los usuarios es un pilar crítico para la experiencia del cliente y la continuidad operativa. Ya sea la confirmación de un pedido, una alerta de seguridad o una campaña promocional, el sistema requiere una infraestructura de mensajería flexible.

Este **Componente de Gestión de Notificaciones** nace como una solución arquitectónica centralizada para resolver los problemas comunes de los sistemas de envío tradicionales, tales como el acoplamiento rígido a proveedores específicos y la interrupción de flujos de trabajo debido a caídas de red unificadas. 

Al adoptar un enfoque modular, este componente abstrae la complejidad de las conexiones externas (APIs de terceros), garantizando que el negocio pueda comunicarse a través de múltiples canales de manera simultánea, tolerante a fallos y altamente escalable en el tiempo.

---

## 📋 Requisitos del Sistema

### Requisitos Funcionales (RF)
*   **RF-01 (4 Canales independientes):** Despacho a través de Email, SMS, Push Notifications y WhatsApp, aplicando formateo independiente según el proveedor.
*   **RF-02 (Envío simultáneo):** Capacidad paralela/concurrente para enviar un único mensaje a múltiples canales simultáneamente.
*   **RF-03 (Logging centralizado):** Registro persistente de cada intento con estampa de tiempo, canal, destinatario y resultado (éxito/falla).
*   **RF-04 (Gestión aislada de errores):** Captura local de excepciones por canal; si un proveedor cae, los canales restantes no interrumpen su flujo.

### Requerimientos Técnicos (RT)
*   **RT-01 (Principios SOLID):** Implementación rigurosa de SRP, OCP y DIP.
*   **RT-02 (Composición sobre Herencia):** Orquestación mediante colecciones dinámicas acopladas en tiempo de ejecución.
*   **RT-03 (Alta cohesión y Bajo acoplamiento):** Comunicación estricta mediante contratos abstractos.
*   **RT-04 (Diseño por Contrato):** Validación explícita de precondiciones y postcondiciones en funciones críticas.

---

## 🏗️ Composición sobre Herencia

Para este componente se priorizó la **Composición** frente a la Herencia con el fin de evitar jerarquías rígidas y código duplicado.

| Enfoque | Relación | Ventaja en TechSolutions | Desventaja en TechSolutions |
| :--- | :--- | :--- | :--- |
| **Herencia** | Es un (*Is-a*) | Estructura jerárquica simple al inicio. | Rígido. Fuerza clases híbridas complejas para envíos combinados (ej: `EmailAndSMSNotification`). |
| **Composición** | Tiene un (*Has-a*) | **Alta flexibilidad.** Inyección dinámica de canales para envíos multicanal simultáneos. | Mayor cantidad de interfaces iniciales para el desarrollo. |

### Justificación Técnico-Arquitectónica:
1. **Elimina el acoplamiento:** Desvincula el tipo de mensaje de la lógica de red de cada proveedor.
2. **Flexibilidad en Ejecución:** `NotificationService` administra una lista dinámica de canales; se pueden activar o desactivar módulos en caliente sin alterar el núcleo del sistema.

---

## 🛠️ Arquitectura SOLID pipelines y Estructura del Repositorio

La organización del código fuente en la carpeta `app/` refleja directamente las responsabilidades del diseño arquitectónico:

```text
├── app/
│   ├── api/
│   │   └── endpoints.py           # Endpoints expuestos de la API externa
│   ├── core/
│   │   └── interfaces.py          # Interfaces puras del sistema (DIP / Diseño por Contrato)
│   ├── infrastructure/
│   │   ├── email_sender.py        # Implementación concreta del canal de Email (SRP)
│   │   ├── sms_sender.py          # Implementación concreta del canal de SMS (SRP)
│   │   ├── push_sender.py         # Implementación concreta del canal de Push (SRP)
│   │   ├── whatsapp_sender.py     # Implementación concreta del canal de WhatsApp (SRP)
│   │   └── file_logger.py         # Infraestructura de logging centralizado (SRP)
│   ├── services/
│   │   └── notification_service.py # Clase Orquestadora central (OCP)
│   └── main.py                    # Punto de entrada de la aplicación
├── tests/                         # Suite de pruebas automatizadas unitarias
├── .gitignore
├── README.md
└── requirements.txt
```

### Mapeo de Principios SOLID
*   **S – Single Responsibility Principle (SRP):** Cada archivo en `infrastructure/` encapsula una sola funcionalidad. Modificar la API de un proveedor externo no impacta colateralmente a los demás canales.
*   **O – Open/Closed Principle (OCP):** Implementado en `notification_service.py` mediante el método `register_channel`. El motor central está cerrado a modificaciones pero abierto a extensiones (ej. añadir Telegram o Slack sin tocar el código núcleo).
*   **D – Dependency Inversion Principle (DIP):** El servicio de alto nivel (`NotificationService`) depende exclusivamente de la abstracción `INotificationSender` definida en `core/interfaces.py`, aislando la lógica de negocio de las librerías de infraestructura de bajo nivel.

---

## 📑 Diseño por Contrato (Design by Contract)

### 🔏 Interfaz: `INotificationSender`
#### Método: `send(destination: str, message: str) -> bool`
*   **Precondiciones:**
    *   `destination` no puede ser nulo, vacío ni contener solo espacios en blanco.
    *   `message` no puede ser nulo, vacío, ni superar el límite preventivo de 1000 caracteres.
*   **Postcondiciones:**
    *   Retorna `True` si la pasarela aceptó el mensaje, `False` si fue rechazado.
    *   El estado interno del canal no debe corromperse en caso de error de red.

### 🗃️ Servicio: `NotificationService`
#### Método: `send_multichannel(destinations: dict, message: str) -> dict`
*   **Precondiciones:**
    *   `destinations` debe poseer al menos un par clave-valor válido (ej: `{"email": "user@test.com"}`).
    *   Las llaves deben corresponder estrictamente a canales previamente registrados.
    *   `message` debe cumplir con los criterios de validez y tamaño de la interfaz base.
*   **Postcondiciones:**
    *   Retorna un diccionario detallando el estado individual por canal (ej: `{"email": "Enviado con éxito"}`).
    *   Genera un **registro obligatorio** en el `file_logger` con los datos de auditoría de la transacción.

---

## ⚙️ Instalación y Configuración

Siga estos pasos para preparar y desplegar el entorno de desarrollo en su máquina local:

### 1. Clonar el repositorio
```bash
git clone https://github.com
cd PA_IS_3
```

### 2. Configurar el Entorno Virtual de Python
Se recomienda el uso de entornos aislados para evitar conflictos de dependencias en el sistema de desarrollo:

```bash
# En sistemas basados en Linux / macOS
python3 -m venv venv
source venv/bin/activate

# En sistemas Windows (PowerShell / CMD)
python -m venv venv
.\venv\Scripts\activate
```

### 3. Instalar dependencias del proyecto
Instale el conjunto de herramientas requeridas (como gestores de pruebas o utilidades) declaradas en el manifiesto técnico:
```bash
pip install -r requirements.txt
```

---

## 💻 Guía de Uso

Para instanciar el orquestador principal e interactuar con los diferentes canales de mensajería inyectados, puede inicializar la ejecución del núcleo mediante el comando de inicio en la raíz de su terminal:

```bash
python -m app.services.notification_service
```

*(Nota: Alternativamente, puede importar de forma directa el motor central en cualquier módulo del ecosistema TechSolutions de la siguiente manera)*:

```python
from app.services.notification_service import NotificationService
from app.infrastructure.email_sender import EmailSender
from app.infrastructure.sms_sender import SmsSender

# 1. Instanciar el servicio núcleo
servicio_notificaciones = NotificationService()

# 2. Registrar los canales dinámicamente mediante composición (OCP)
servicio_notificaciones.register_channel("email", EmailSender())
servicio_notificaciones.register_channel("sms", SmsSender())

# 3. Disparar envíos multicanal concurrentes
destinatarios = {
    "email": "cliente@techsolutions.com",
    "sms": "+51999888777"
}
resultado = servicio_notificaciones.send_multichannel(destinatarios, "Su pedido ha sido procesado con éxito.")
print(resultado)
```

---

## 🧪 Ejecución de Pruebas Unitarias y Cobertura (Coverage)

La carpeta `tests/` valida de manera automática el aislamiento y la captura de errores específicos por canal (RF-04), así como los contratos obligatorios de entrada y salida (RT-04). 

### Ejecución básica de pruebas
Para ejecutar las pruebas del repositorio:
```bash
pytest
```

### Generación del reporte de Cobertura
Para auditar qué tanto porcentaje de tu código está cubierto por las pruebas unitarias y desplegar el informe tabular en la terminal, ejecuta:
```bash
pytest --cov=app --cov-report=term
```
