from .base_agent import KnifeStoreAgent, CONVERSATION_EXAMPLES

class SalesAgent(KnifeStoreAgent):
    def __init__(self):
        super().__init__(
            name="Agente de Ventas",
            role="Especialista en Ventas de Cuchillos",
            goal="Ayudar a los clientes a encontrar el cuchillo perfecto para sus necesidades y cerrar ventas",
            backstory="""
            Soy un experto en cuchillería con años de experiencia en la venta de cuchillos de alta calidad.
            Conozco a fondo cada producto, sus características, usos y beneficios.
            Mi objetivo es asegurar que cada cliente encuentre exactamente el cuchillo que necesita,
            proporcionando información detallada y respondiendo todas sus preguntas de manera profesional y amigable.
            """,
            verbose=True
        )
    
    async def handle_product_inquiry(self, message: str) -> str:
        """
        Maneja consultas específicas sobre productos
        """
        prompt = f"""
        Como experto en cuchillos, responde a la siguiente consulta del cliente de forma CONCISA:
        
        {message}
        
        Instrucciones importantes:
        - Sé breve y directo, máximo 2-3 oraciones
        - NO repitas la pregunta del cliente en tu respuesta
        - Si el mensaje incluye "Conversación reciente", mantén coherencia con esa conversación previa
        - SIEMPRE que veas "Información real del producto", UTILIZA ESA INFORMACIÓN como FUENTE PRINCIPAL
        - NO INVENTES productos ni información que no se te proporcione explícitamente
        - SÓLO recomienda productos que aparecen en la información de productos proporcionada
        - Si no hay información sobre productos específicos, no menciones nombres de productos
        - Responde ÚNICAMENTE a la "Consulta actual del cliente", no a todo el contexto
        - Mantén un tono amigable pero profesional 
        - Usa "vos" en lugar de "usted"
        - NO utilices emojis en tus respuestas
        
        Aquí hay ejemplos del estilo de comunicación, pero RECUERDA SER MÁS CONCISO que estos ejemplos:
        {CONVERSATION_EXAMPLES}
        """
        return await self.analyze_message(prompt)
    
    async def handle_use_case_inquiry(self, message: str, available_products: str) -> str:
        """
        Maneja consultas sobre recomendaciones para casos de uso específicos (cocina, asado, etc.)
        basándose SOLAMENTE en los productos disponibles reales
        """
        prompt = f"""
        Como experto en cuchillos, recomienda productos ÚNICAMENTE de la lista de productos disponibles:
        
        Consulta del cliente: {message}
        
        Productos disponibles:
        {available_products}
        
        Instrucciones críticas:
        - NUNCA recomiendes un producto que no esté en la lista de productos disponibles
        - NUNCA inventes productos ni características
        - Sé breve y directo, máximo 2 oraciones
        - Recomienda solo productos específicos de la lista por su nombre exacto
        - Si no hay productos adecuados para el caso consultado, dilo honestamente
        - NO menciones cuchillos o tipos que no estén en la lista
        - Usa "vos" en lugar de "usted"
        - Si varios productos de la lista sirven, menciona máximo 2
        - NO utilices emojis en tus respuestas
        """
        return await self.analyze_message(prompt)
    
    async def handle_price_inquiry(self, product: str) -> str:
        """
        Maneja consultas específicas sobre precios
        """
        prompt = f"""
        Responde a la siguiente consulta sobre precios de manera CONCISA:
        
        {product}
        
        Instrucciones importantes:
        - Sé breve y directo, máximo 2-3 oraciones
        - Si el mensaje incluye "Conversación reciente", mantén coherencia con esa conversación previa
        - Responde ÚNICAMENTE a la "Consulta actual del cliente", no a todo el contexto
        - NO repitas la pregunta del cliente en tu respuesta
        - SIEMPRE que veas "Información real del producto", UTILIZA ESA INFORMACIÓN como la ÚNICA fuente válida para el precio
        - NO INVENTES productos ni información que no se te proporcione explícitamente
        - Menciona el precio específico exactamente como aparece en la información real
        - Un solo detalle adicional del producto si es relevante
        - Usa "vos" en lugar de "usted"
        - NO utilices emojis en tus respuestas
        
        Aquí hay ejemplos del estilo de comunicación, pero RECUERDA SER MÁS CONCISO que estos ejemplos:
        {CONVERSATION_EXAMPLES}
        """
        return await self.analyze_message(prompt)
    
    async def handle_payment_inquiry(self, message: str) -> str:
        """
        Maneja consultas sobre métodos de pago y procesos de compra
        con mayor comprensión contextual
        """
        prompt = f"""
        Como especialista en ventas, responde a esta consulta sobre métodos de pago:
        
        {message}
        
        Instrucciones importantes:
        - ANALIZA cuidadosamente el contexto de la conversación
        - NO PREGUNTES por el método de pago si el cliente está todavía explorando productos o pidiendo catálogo
        - Si el mensaje contiene términos como "mostrar", "ver", "catálogo", "lista" o "todos los cuchillos", recomienda NO RESPONDER sobre métodos de pago y sugerir ver el catálogo primero
        - Si el cliente está diciendo que aún no está listo para pagar, RESPETA eso y vuelve al proceso de selección de productos
        - Si el mensaje contiene "la primera" o "primera opción", interpreta que está eligiendo pago en EFECTIVO
        - Si el mensaje contiene "la segunda" o "segunda opción", interpreta que está eligiendo TRANSFERENCIA 
        - Si menciona explícitamente "efectivo", proporciona información para pago en tienda
        - Si menciona explícitamente "transferencia", proporciona los datos bancarios
        - Si está preguntando específicamente por opciones de pago, enumera ambas posibilidades
        - NO INVENTES información bancaria o de direcciones, usa estos datos exactos:
          * Efectivo: Av. Ejemplo 1234, Ciudad - Lunes a Viernes 9:00 a 18:00
          * Transferencia: Banco Nacional, Titular: Cuchillos Premium S.A., CBU/ALIAS: CUCHILLOS.PREMIUM, CUIT: 30-12345678-9
        - Sé claro, directo y natural en tu respuesta
        - Usa "vos" en lugar de "usted"
        - NO utilices emojis en tu respuesta
        - Limita tu respuesta a 3-4 oraciones máximo
        """
        return await self.analyze_message(prompt) 