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
        - Proporciona información precisa basada en los datos proporcionados
        - Responde ÚNICAMENTE a la "Consulta actual del cliente", no a todo el contexto
        - Mantén un tono amigable pero profesional 
        - Usa "vos" en lugar de "usted"
        - Incluye máximo un emoji si es apropiado
        
        Aquí hay ejemplos del estilo de comunicación, pero RECUERDA SER MÁS CONCISO que estos ejemplos:
        {CONVERSATION_EXAMPLES}
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
        - Menciona el precio específico exactamente como aparece en la información real
        - Un solo detalle adicional del producto si es relevante
        - Usa "vos" en lugar de "usted"
        - Incluye máximo un emoji si es apropiado
        
        Aquí hay ejemplos del estilo de comunicación, pero RECUERDA SER MÁS CONCISO que estos ejemplos:
        {CONVERSATION_EXAMPLES}
        """
        return await self.analyze_message(prompt) 