import google.generativeai as genai
from dotenv import load_dotenv
import os
import logging
from app.data.examples import SAMPLE_CONVERSATIONS

logger = logging.getLogger(__name__)

load_dotenv()

# Configurar Gemini
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    logger.error("No se encontró la API key de Gemini. Por favor, configura la variable de entorno GEMINI_API_KEY.")
    raise ValueError("GEMINI_API_KEY no está configurada")

genai.configure(api_key=gemini_api_key)

# Definir la configuración del modelo
generation_config = {
    "temperature": 0.0,
    "top_p": 1.0,
    "top_k": 1,
    "max_output_tokens": 1024,
}

# Configurar el modelo de Gemini
gemini_model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config
)

# Crear un contexto con ejemplos de conversaciones para el modelo
def get_conversation_examples():
    examples = ""
    for idx, convo in enumerate(SAMPLE_CONVERSATIONS, 1):
        examples += f"\nEjemplo {idx}:\n"
        examples += f"Cliente: {convo['client']}\n"
        examples += f"Dueño: {convo['owner']}\n"
    return examples

CONVERSATION_EXAMPLES = get_conversation_examples()

class KnifeStoreAgent:
    """
    Agente base para la tienda de cuchillos.
    Usa Gemini directamente en lugar de CrewAI.
    """
    
    def __init__(
        self,
        name: str,
        role: str,
        goal: str,
        backstory: str,
        verbose: bool = False,
    ):
        self.name = name
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.verbose = verbose
        
        if self.verbose:
            logger.info(f"Agente {self.name} inicializado")
    
    async def analyze_message(self, message: str) -> str:
        """
        Analiza un mensaje usando el modelo de Gemini
        """
        try:
            if self.verbose:
                logger.info(f"Analizando mensaje: {message[:50]}...")
                
            response = await gemini_model.generate_content_async(message)
            
            if self.verbose:
                logger.info(f"Respuesta obtenida: {response.text[:50]}...")
                
            return response.text
        except Exception as e:
            error_msg = f"Error al analizar mensaje: {e}"
            logger.error(error_msg)
            return "Lo siento, hubo un error al procesar tu mensaje."