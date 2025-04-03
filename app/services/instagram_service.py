import json
import os
from typing import Dict, Any
from app.agents.agent_manager import AgentManager
from app.services.product_service import ProductService
from app.services.conversation_service import ConversationService
from app.database.database import SessionLocal

class InstagramService:
    """
    Servicio para manejar la integración con Instagram Direct API
    (Actualmente mockeado)
    """
    
    def __init__(self):
        self.agent_manager = AgentManager()
        # Mock storage para mensajes
        self.messages = []
        # Inicializar servicio de productos
        self.db = SessionLocal()
        self.product_service = ProductService(self.db)
        # Inicializar servicio de conversaciones
        self.conversation_service = ConversationService()
        
    def __del__(self):
        """Cerrar la sesión de base de datos al destruir el objeto"""
        if hasattr(self, 'db'):
            self.db.close()
    
    async def process_incoming_message(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa un mensaje entrante de Instagram y genera una respuesta
        
        Args:
            message_data: Datos del mensaje recibido
           
        Returns:
            Dict con la respuesta generada
        """
        try:
            # Extraer el texto del mensaje (formato simulado de Instagram)
            message_text = message_data.get("message", {}).get("text", "")
            sender = message_data.get("message", {}).get("from", "unknown")
            
            # Guardar el mensaje recibido
            self.messages.append({
                "sender": sender,
                "text": message_text,
                "timestamp": message_data.get("timestamp", ""),
                "type": "received",
                "platform": "instagram"
            })
            
            # Agregar mensaje al historial de conversación
            self.conversation_service.add_message(sender, message_text, "user")
            
            # Obtener contexto de la conversación
            conversation_context = self.conversation_service.get_conversation_context(sender)
            
            # Procesar casos especiales para lista de productos o información de producto
            response_text = ""
            
            # Verificar si es una consulta sobre toda la lista de productos
            if any(keyword in message_text.lower() for keyword in 
                  ["lista de productos", "listado de cuchillos", "todos los cuchillos", 
                   "catálogo", "catalogo", "qué cuchillos tienen", "que cuchillos tienen",
                   "qué productos tienen", "que productos tienen", "listado completo", 
                   "productos con sus precios", "lista con precios", "listado de precios",
                   "precios de todos", "mostrar productos", "ver productos"]):
                products_text = self.product_service.get_all_products_text()
                response_text = f"¡Acá está nuestro catálogo actual! 🔪\n\n{products_text}"
            
            # Si no hay respuesta especial, procesar el mensaje con nuestros agentes
            if not response_text:
                # Procesar el mensaje con nuestros agentes
                classification = await self.agent_manager.classifier_agent.classify_message(message_text)
                
                # Verificar si es una consulta sobre precios de productos mencionados anteriormente
                price_reference_keywords = ["precios", "cuestan", "cuanto", "valor", "cuánto valen", "valen", "precio"]
                reference_keywords = ["esos", "estos", "que me mencionas", "mencionados", "anteriores", "que dijiste"]
                
                is_price_reference_query = any(price_kw in message_text.lower() for price_kw in price_reference_keywords) and \
                                          any(ref_kw in message_text.lower() for ref_kw in reference_keywords)
                
                # Si es una consulta de precios con referencia a productos anteriores
                if is_price_reference_query:
                    # Buscar productos mencionados en mensajes anteriores del bot
                    previous_messages = self.conversation_service.get_conversation_history(sender, 10)
                    mentioned_products = []
                    
                    for msg in previous_messages:
                        if msg["role"] == "bot":
                            # Intentar extraer nombres de productos de mensajes anteriores
                            bot_response = msg["content"].lower()
                            # Buscar productos en la base de datos y verificar cuáles se mencionaron
                            all_products = self.product_service.get_all_products()
                            for product in all_products:
                                if product.name.lower() in bot_response:
                                    mentioned_products.append(product.name)
                    
                    # Si encontramos productos mencionados anteriormente
                    if mentioned_products:
                        products_info = []
                        for product_name in mentioned_products:
                            info = self.product_service.get_product_info_by_name(product_name)
                            products_info.append(info)
                        
                        combined_info = "\n".join(products_info)
                        response_text = f"Claro, estos son los precios de los productos que mencioné:\n\n{combined_info}"
                
                # Si no es una consulta de referencia o no se encontraron productos
                if not response_text:
                    # Si se mencionó un producto específico y es una consulta de precio o producto
                    if classification["product_mentioned"] and classification["type"] == "sales":
                        # Agregar información real del producto mencionado
                        product_info = self.product_service.get_product_info_by_name(classification["product_mentioned"])
                        extra_info = f"\n\nInformación real del producto: {product_info}"
                        
                        # Incluir el contexto de la conversación
                        full_context = f"""
                        {conversation_context}
                        
                        Consulta actual del cliente: {message_text}
                        {extra_info}
                        """
                        
                        # Generar respuesta con el agente, incluyendo la información real
                        if classification["subtype"] == "price_inquiry":
                            base_response = await self.agent_manager.sales_agent.handle_price_inquiry(full_context)
                        else:
                            base_response = await self.agent_manager.sales_agent.handle_product_inquiry(full_context)
                        
                        response_text = base_response
                    else:
                        # Incluir el contexto de la conversación
                        full_context = f"""
                        {conversation_context}
                        
                        Consulta actual del cliente: {message_text}
                        """
                        response_text = await self.agent_manager.process_message(full_context)
            
            # Guardar la respuesta en el historial de conversación
            self.conversation_service.add_message(sender, response_text, "bot")
            
            # Guardar la respuesta en el registro de mensajes
            self.messages.append({
                "sender": "bot",
                "text": response_text,
                "timestamp": "",
                "type": "sent",
                "platform": "instagram"
            })
            
            # Crear una respuesta simulada
            response = {
                "recipient_id": sender,
                "message_id": f"ig_msg_{len(self.messages)}",
                "message": response_text,
                "status": "sent"
            }
            
            return response
            
        except Exception as e:
            print(f"Error procesando mensaje de Instagram: {e}")
            return {
                "recipient_id": sender,
                "message_id": "error",
                "message": "Lo siento, ocurrió un error al procesar tu mensaje. Por favor, inténtalo de nuevo.",
                "status": "error"
            }
    
    def get_conversation_history(self, sender_id: str) -> list:
        """
        Obtener el historial de conversación con un remitente específico
        """
        return [msg for msg in self.messages if msg.get("sender") == sender_id or 
               (msg.get("sender") == "bot" and msg.get("type") == "sent")] 