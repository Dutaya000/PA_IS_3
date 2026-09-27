from fastapi import FastAPI
from app.api.endpoints import router as api_router

app = FastAPI(
    title="TechSolutions Notification Component API",
    version="1.0.0"
)

# Acoplamos el enrutador a la aplicación principal
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "El componente está corriendo con éxito. Visita /docs para Swagger UI."}
