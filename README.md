# WhatsApp Bot para Tienda de Cuchillos

Un asistente virtual para atención al cliente de una tienda de cuchillos implementado como un bot de WhatsApp.

## Características

- Sistema de procesamiento de mensajes de WhatsApp
- Agentes específicos para ventas y soporte
- Integración con base de datos de productos
- Manejo de conversaciones con memoria de contexto
- Respuestas concisas y naturales

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/whatsapp_bot.git
cd whatsapp_bot
```

2. Crear un entorno virtual e instalar dependencias:
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Configurar la base de datos:
```bash
python app/database/init_db.py
```

## Uso

Ejecutar la aplicación:
```bash
python run.py
```

La aplicación se ejecutará en http://127.0.0.1:8081

## Estructura del Proyecto

- `app/` - Código principal de la aplicación
  - `agents/` - Agentes IA (ventas, soporte, clasificador)
  - `database/` - Configuración y modelos de base de datos
  - `models/` - Modelos de datos
  - `services/` - Servicios de aplicación
  - `tests/` - Pruebas unitarias
- `run.py` - Punto de entrada principal

## Créditos

Desarrollado por [Tu Nombre] 