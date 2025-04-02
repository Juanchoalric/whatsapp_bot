from .base_agent import KnifeStoreAgent, CONVERSATION_EXAMPLES

class ClassifierAgent(KnifeStoreAgent):
    def __init__(self):
        super().__init__(
            name="Agente Clasificador",
            role="Clasificador de Mensajes",
            goal="Analizar el contenido de los mensajes y determinar su intención principal",
            backstory="""
            Soy un experto en análisis de lenguaje natural, especializado en entender la intención
            detrás de los mensajes de los clientes. Mi trabajo es determinar rápidamente qué tipo
            de consulta está haciendo el cliente para dirigirla al agente más adecuado. Tengo un
            profundo entendimiento de las diferentes categorías de consultas que pueden realizarse
            en una tienda de cuchillos.
            """,
            verbose=True
        )
    
    async def classify_message(self, message: str) -> dict:
        """
        Clasifica el mensaje según su intención y contenido
        
        Returns:
            dict: Un diccionario con la clasificación y confianza
                {
                    "type": "sales|support|general",
                    "subtype": "product_inquiry|price_inquiry|shipping|etc",
                    "confidence": float,
                    "product_mentioned": str (opcional)
                }
        """
        prompt = f"""
        Clasifica este mensaje de un cliente de una tienda de cuchillos:
        "{message}"
        
        Responde SOLO con un JSON con este formato exacto:
        {{
            "type": "sales o support o general",
            "subtype": "product_inquiry o price_inquiry o shipping o return o complaint o general_question",
            "confidence": [valor entre 0.0 y 1.0],
            "product_mentioned": "[nombre del producto si se menciona alguno, o null si no]"
        }}
        
        NO incluyas ningún texto adicional, solo el JSON.
        """
        
        response = await self.analyze_message(prompt)
        
        try:
            # Limpiar la respuesta en caso de que venga con formato incorrecto
            import json
            import re
            
            # Intentar encontrar el JSON en la respuesta
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                classification = json.loads(json_str)
                return classification
            else:
                # Si no se puede encontrar un JSON válido, devuelve una clasificación por defecto
                return {
                    "type": "general",
                    "subtype": "general_question",
                    "confidence": 0.5,
                    "product_mentioned": None
                }
        except Exception as e:
            print(f"Error al parsear la clasificación: {e}")
            return {
                "type": "general",
                "subtype": "general_question",
                "confidence": 0.5,
                "product_mentioned": None
            } 