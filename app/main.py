from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from dotenv import load_dotenv
import os
import uvicorn
import logging

from app.services.whatsapp_service import WhatsAppService
from app.services.instagram_service import InstagramService
from app.database.database import get_db, engine, Base
from app.database.seed_data import seed_database
from sqlalchemy.orm import Session

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Inicializar la aplicación
app = FastAPI(title="Cuchillos Bot API", description="API para bot multiplataforma de venta de cuchillos")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Inicializar los servicios de mensajería
whatsapp_service = None
instagram_service = None

@app.on_event("startup")
async def startup_event():
    """
    Inicializa la base de datos y servicios al iniciar la aplicación
    """
    global whatsapp_service, instagram_service
    try:
        # Crear tablas y poblar la base de datos
        logger.info("Inicializando base de datos...")
        seed_database()
        logger.info("Base de datos inicializada correctamente")
        
        # Inicializar el servicio de WhatsApp
        logger.info("Inicializando servicios de mensajería...")
        whatsapp_service = WhatsAppService()
        instagram_service = InstagramService()
        logger.info("Servicios de mensajería inicializados correctamente")
    except Exception as e:
        logger.error(f"Error durante la inicialización: {e}")
        raise

@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Redirecciona a la interfaz de prueba
    """
    return RedirectResponse(url="/static/index.html")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/webhook")
async def webhook_handler(request: Request):
    """
    Endpoint para recibir mensajes de WhatsApp
    """
    if not whatsapp_service:
        raise HTTPException(status_code=503, detail="Servicio WhatsApp no disponible")
        
    try:
        body = await request.json()
        response = await whatsapp_service.process_incoming_message(body)
        return response
    except Exception as e:
        logger.error(f"Error en webhook: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/messages/{sender_id}")
async def get_messages(sender_id: str):
    """
    Endpoint para obtener el historial de mensajes con un remitente
    """
    if not whatsapp_service:
        raise HTTPException(status_code=503, detail="Servicio WhatsApp no disponible")
        
    messages = whatsapp_service.get_conversation_history(sender_id)
    return {"messages": messages}

# Endpoint para probar el bot manualmente
@app.post("/test-message")
async def test_message(message: dict):
    """
    Endpoint para probar el bot directamente sin WhatsApp
    Ejemplo de cuerpo de solicitud:
    {
        "message": {
            "text": "Hola, quiero información sobre sus cuchillos",
            "from": "test_user"
        }
    }
    """
    if not whatsapp_service:
        raise HTTPException(status_code=503, detail="Servicio WhatsApp no disponible")
        
    try:
        response = await whatsapp_service.process_incoming_message(message)
        return response
    except Exception as e:
        logger.error(f"Error en test-message: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/instagram-webhook")
async def instagram_webhook_handler(request: Request):
    """
    Endpoint para recibir mensajes de Instagram
    """
    if not instagram_service:
        raise HTTPException(status_code=503, detail="Servicio Instagram no disponible")
        
    try:
        body = await request.json()
        response = await instagram_service.process_incoming_message(body)
        return response
    except Exception as e:
        logger.error(f"Error en Instagram webhook: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/instagram-messages/{sender_id}")
async def get_instagram_messages(sender_id: str):
    """
    Endpoint para obtener el historial de mensajes de Instagram con un remitente
    """
    if not instagram_service:
        raise HTTPException(status_code=503, detail="Servicio Instagram no disponible")
        
    messages = instagram_service.get_conversation_history(sender_id)
    return {"messages": messages}

# Endpoint para probar el bot de Instagram manualmente
@app.post("/test-instagram")
async def test_instagram(message: dict):
    """
    Endpoint para probar el bot de Instagram directamente
    Ejemplo de cuerpo de solicitud:
    {
        "message": {
            "text": "Hola, quiero información sobre sus cuchillos",
            "from": "instagram_user"
        }
    }
    """
    if not instagram_service:
        raise HTTPException(status_code=503, detail="Servicio Instagram no disponible")
        
    try:
        response = await instagram_service.process_incoming_message(message)
        return response
    except Exception as e:
        logger.error(f"Error en test-instagram: {e}")
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 