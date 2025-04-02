from .sales_agent import SalesAgent
from .support_agent import SupportAgent
from .classifier_agent import ClassifierAgent
import logging

logger = logging.getLogger(__name__)

class AgentManager:
    """
    Clase que coordina el trabajo entre diferentes agentes
    """
    
    def __init__(self):
        try:
            logger.info("Inicializando agentes...")
            self.sales_agent = SalesAgent()
            self.support_agent = SupportAgent()
            self.classifier_agent = ClassifierAgent()
            logger.info("Agentes inicializados correctamente")
        except Exception as e:
            logger.error(f"Error al inicializar agentes: {e}")
            raise
    
    async def process_message(self, message: str) -> str:
        """
        Procesa un mensaje recibido y devuelve una respuesta generada por el agente apropiado
        """
        try:
            # Si el mensaje está vacío, devolvemos un mensaje de error
            if not message or message.strip() == "":
                return "Lo siento, no he recibido ningún mensaje. ¿En qué puedo ayudarte?"
                
            logger.info(f"Procesando mensaje: {message[:50]}...")
            
            # Primero clasificamos el mensaje
            classification = await self.classifier_agent.classify_message(message)
            logger.info(f"Clasificación: {classification}")
            
            # Determinamos qué agente debe manejar el mensaje
            if classification["type"] == "sales":
                if classification["subtype"] == "price_inquiry" and classification["product_mentioned"]:
                    response = await self.sales_agent.handle_price_inquiry(classification["product_mentioned"])
                else:
                    response = await self.sales_agent.handle_product_inquiry(message)
                    
            elif classification["type"] == "support":
                if classification["subtype"] == "shipping":
                    response = await self.support_agent.handle_shipping_inquiry(message)
                else:
                    response = await self.support_agent.handle_general_inquiry(message)
                    
            # Por defecto, usamos el agente de soporte para consultas generales
            else:
                response = await self.support_agent.handle_general_inquiry(message)
                
            logger.info(f"Respuesta generada: {response[:50]}...")
            return response
            
        except Exception as e:
            logger.error(f"Error al procesar mensaje: {e}")
            return "Lo siento, tuve un problema al procesar tu mensaje. ¿Podrías intentar nuevamente con otras palabras?" 