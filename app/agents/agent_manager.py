from .sales_agent import SalesAgent
from .support_agent import SupportAgent
from .classifier_agent import ClassifierAgent
from app.database.database import SessionLocal
from app.services.product_service import ProductService
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
            # Inicializar servicio de productos para consulta directa
            self.db = SessionLocal()
            self.product_service = ProductService(self.db)
            logger.info("Agentes inicializados correctamente")
        except Exception as e:
            logger.error(f"Error al inicializar agentes: {e}")
            raise
    
    def __del__(self):
        """Cerrar la sesión de base de datos al destruir el objeto"""
        if hasattr(self, 'db'):
            self.db.close()
    
    async def process_message(self, message: str) -> str:
        """
        Procesa un mensaje recibido y devuelve una respuesta generada por el agente apropiado
        """
        try:
            # Si el mensaje está vacío, devolvemos un mensaje de error
            if not message or message.strip() == "":
                return "Lo siento, no he recibido ningún mensaje. ¿En qué puedo ayudarte?"
                
            logger.info(f"Procesando mensaje: {message[:50]}...")
            
            # Verificar si es una consulta sobre métodos de pago o proceso de compra
            payment_keywords = ["pagar", "pagarlo", "comprar", "comprarlo", "adquirir", "adquirirlo", "método de pago", "forma de pago", 
                                "efectivo", "transferencia", "tarjeta", "crédito", "débito"]
            purchase_process_keywords = ["compra", "pago", "pedido", "orden", "envío", "retirar", "retiro"]

            is_payment_query = any(keyword in message.lower() for keyword in payment_keywords)

            # Referencias a opciones como "la primera" o "la segunda"
            option_references = ["primera", "primero", "opción 1", "segunda", "segundo", "opción 2", "número 1", "número 2", "numero 1", "numero 2"]
            is_option_reference = any(option in message.lower() for option in option_references)

            # Referencias a catálogo/lista de productos
            catalog_keywords = ["mostrame todos", "mostrar todos", "ver todos", "catalogo", "catálogo", "lista", "todos los cuchillos", 
                                "todos los productos", "que cuchillos", "qué cuchillos", "disponibles"]

            # Si es una consulta para ver todos los productos
            if any(keyword in message.lower() for keyword in catalog_keywords):
                # Obtener todos los productos disponibles
                all_products = self.product_service.get_all_products()
                in_stock_products = [p for p in all_products if p.stock > 0]
                
                if not in_stock_products:
                    return "Actualmente no tenemos cuchillos en stock. Te avisaremos cuando recibamos nuevos productos."
                
                response = "CATÁLOGO DE PRODUCTOS DISPONIBLES:\n\n"
                for product in in_stock_products:
                    response += f"""{product.name}
Precio: ${product.price:.2f}
Stock: {product.stock} unidades disponibles

"""
                
                return response

            # Si es una consulta de pago o una referencia a opciones, usar el agente de ventas con el método especializado
            if is_payment_query or is_option_reference:
                response = await self.sales_agent.handle_payment_inquiry(message)
                return response
            
            # Primero clasificamos el mensaje
            classification = await self.classifier_agent.classify_message(message)
            logger.info(f"Clasificación: {classification}")
            
            # Verificar si se menciona un producto específico
            product_mentioned = classification.get("product_mentioned")
            
            # Si se menciona un producto, verificar si existe en la base de datos
            real_product_info = None
            if product_mentioned:
                # Corregir errores ortográficos comunes
                product_mentioned_clean = product_mentioned.lower().replace("chuchillo", "cuchillo")
                
                # Verificar si el producto existe en la base de datos - ahora con mayor tolerancia a errores
                products = self.product_service.get_products_by_name(product_mentioned_clean)
                if products:
                    # Si existe, usar la información real
                    real_product_info = f"Producto encontrado en la base de datos: {products[0].name}, Precio: ${products[0].price:.2f}, Stock: {products[0].stock}"
                else:
                    # Si el producto no existe en la base de datos
                    real_product_info = f"El producto '{product_mentioned}' no existe en nuestro catálogo."
                    
                # Si es una consulta de precio, responder directamente con la información de la base de datos
                if classification["type"] == "sales" and classification["subtype"] == "price_inquiry":
                    if products:
                        product = products[0]
                        if product.stock > 0:
                            return f"El {product.name} cuesta ${product.price:.2f} y tenemos {product.stock} unidades disponibles."
                        else:
                            return f"El {product.name} cuesta ${product.price:.2f} pero actualmente no tenemos stock. Te avisamos cuando vuelva a estar disponible."
                    else:
                        return f"Lo siento, no tenemos '{product_mentioned}' en nuestro catálogo. ¿Te puedo ayudar con algún otro cuchillo?"
            
            # Determinamos qué agente debe manejar el mensaje
            if classification["type"] == "sales":
                # Verificar si es una consulta sobre casos de uso específicos (asado, cocina, etc.)
                use_case_keywords = ["para", "necesito", "busco", "recomendacion", "mejor para", "adecuado para", "ideal para"]
                context_keywords = ["asado", "cocina", "chef", "pan", "carne", "filetear", "cortar", "deshuesar", "verduras"]
                
                is_use_case_query = any(keyword in message.lower() for keyword in use_case_keywords) and \
                                     any(context in message.lower() for context in context_keywords)
                
                # Si es una pregunta sobre disponibilidad de productos en general
                if "disponibles" in message.lower() or "en stock" in message.lower() or "que cuchillos tenes" in message.lower():
                    # Obtener todos los productos disponibles
                    all_products = self.product_service.get_all_products()
                    in_stock_products = [p for p in all_products if p.stock > 0]
                    
                    if not in_stock_products:
                        return "Actualmente no tenemos cuchillos en stock. Te avisaremos cuando recibamos nuevos productos."
                    
                    response = "CATÁLOGO DE PRODUCTOS DISPONIBLES:\n\n"
                    for product in in_stock_products:
                        response += f"""{product.name}
Precio: ${product.price:.2f}
Stock: {product.stock} unidades disponibles

"""
                    
                    return response
                
                # Si es una consulta sobre precios mencionados genéricamente o múltiples productos
                price_keywords = ["precio", "cuestan", "valen", "cuesta", "precios", "cuanto", "cuánto", "valor"]
                is_general_price_query = any(keyword in message.lower() for keyword in price_keywords)
                
                # Si pregunta por precio sin especificar producto o sobre productos mencionados
                if is_general_price_query:
                    # Caso 1: Pregunta por precios de productos mencionados previamente
                    if "esos" in message.lower() or "los" in message.lower() or "todos" in message.lower() or "me mencionas" in message.lower():
                        # Obtener todos los productos para mostrar precios
                        all_products = self.product_service.get_all_products()
                        in_stock_products = [p for p in all_products if p.stock > 0]
                        
                        if not in_stock_products:
                            return "Actualmente no tenemos cuchillos en stock. Te avisaremos cuando recibamos nuevos productos."
                        
                        response = "LISTA DE PRECIOS:\n\n"
                        for product in in_stock_products:
                            response += f"""{product.name}
Precio: ${product.price:.2f}
Stock: {product.stock} unidades disponibles

"""
                        
                        return response
                    
                    # Caso 2: Pregunta por precio sin especificar producto
                    elif not product_mentioned and message.lower().strip() in ["cual es el precio", "precio?", "precio", "cuanto cuesta", "cuanto vale"]:
                        # Mostrar todos los precios al no especificar producto
                        all_products = self.product_service.get_all_products()
                        in_stock_products = [p for p in all_products if p.stock > 0]
                        
                        if not in_stock_products:
                            return "Actualmente no tenemos cuchillos en stock. Te avisaremos cuando recibamos nuevos productos."
                        
                        response = "¿De cuál cuchillo te interesa saber el precio? Acá están todos nuestros precios:\n\n"
                        for product in in_stock_products:
                            response += f"""{product.name}
Precio: ${product.price:.2f}

"""
                        
                        return response
                
                # Si es una consulta sobre un caso de uso específico (asado, cocina, etc.)
                elif is_use_case_query:
                    # Obtener productos disponibles y filtrarlos según el caso de uso
                    all_products = self.product_service.get_all_products()
                    in_stock_products = [p for p in all_products if p.stock > 0]
                    
                    if not in_stock_products:
                        return "Actualmente no tenemos cuchillos en stock. Te avisaremos cuando recibamos nuevos productos."
                    
                    # Identificar qué productos podrían servir para el caso mencionado
                    relevant_products = []
                    
                    # Determinar el tipo de caso de uso
                    context = ""
                    if "asado" in message.lower():
                        context = "asado"
                        # Para asado, recomendar cuchillos de carne o chef
                        for product in in_stock_products:
                            if "carne" in product.name.lower() or "chef" in product.name.lower():
                                relevant_products.append(product)
                    elif "pan" in message.lower():
                        context = "pan"
                        # Para pan, recomendar cuchillos para pan
                        for product in in_stock_products:
                            if "pan" in product.name.lower():
                                relevant_products.append(product)
                    elif "verdura" in message.lower() or "fruta" in message.lower() or "pelar" in message.lower():
                        context = "verduras/frutas"
                        # Para verduras, recomendar cuchillos puntilla o santoku
                        for product in in_stock_products:
                            if "puntilla" in product.name.lower() or "santoku" in product.name.lower():
                                relevant_products.append(product)
                    
                    # Si no encontramos productos específicos para el caso de uso
                    if not relevant_products:
                        # Si no hay productos específicos, usar el método genérico con todos los productos disponibles
                        products_text = "\n".join([f"{p.name}: {p.description}" for p in in_stock_products])
                        response = await self.sales_agent.handle_use_case_inquiry(message, products_text)
                        return response
                    else:
                        # Si hay productos relevantes, recomendar directamente
                        if len(relevant_products) == 1:
                            product = relevant_products[0]
                            return f"Para {context}, te recomiendo el {product.name} a ${product.price:.2f}. {product.description.split('.')[0]}."
                        else:
                            response = f"Para {context}, te recomiendo estos cuchillos:\n\n"
                            for product in relevant_products[:2]:  # Máximo 2 recomendaciones
                                response += f"{product.name} a ${product.price:.2f}\n"
                                if product.description:
                                    first_sentence = product.description.split('.')[0] + "."
                                    response += f"{first_sentence}\n\n"
                            return response
                
                # Para otras consultas de ventas, usar los agentes con la información real del producto
                if classification["subtype"] == "price_inquiry" and product_mentioned:
                    # Este caso ya fue manejado arriba
                    response = await self.sales_agent.handle_price_inquiry(message + f"\n\n{real_product_info}" if real_product_info else message)
                else:
                    response = await self.sales_agent.handle_product_inquiry(message + f"\n\n{real_product_info}" if real_product_info else message)
                    
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