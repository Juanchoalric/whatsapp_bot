import pytest
import os
from app.agents.sales_agent import SalesAgent
from app.agents.support_agent import SupportAgent

@pytest.mark.asyncio
async def test_concise_product_response():
    """Prueba que las respuestas de productos son concisas"""
    agent = SalesAgent()
    response = await agent.handle_product_inquiry("¿Me podrías decir qué características tiene el cuchillo Santoku?")
    
    # Dividir por puntos para contar oraciones
    sentences = [s.strip() for s in response.split('.') if s.strip()]
    
    # Verificar que la respuesta no es demasiado larga
    assert len(sentences) <= 4, f"La respuesta contiene {len(sentences)} oraciones, debería tener máximo 4"
    
    # Comprobar que no contiene la pregunta original
    assert "qué características" not in response.lower(), "La respuesta repite la pregunta original"
    assert "santoku" in response.lower(), "La respuesta debe mencionar el producto"

@pytest.mark.asyncio
async def test_concise_shipping_response():
    """Prueba que las respuestas de envío son concisas"""
    agent = SupportAgent()
    response = await agent.handle_shipping_inquiry("¿Cuánto tarda el envío a Buenos Aires y cuánto cuesta?")
    
    # Dividir por puntos para contar oraciones
    sentences = [s.strip() for s in response.split('.') if s.strip()]
    
    # Verificar que la respuesta no es demasiado larga
    assert len(sentences) <= 4, f"La respuesta contiene {len(sentences)} oraciones, debería tener máximo 4"
    
    # Comprobar que no contiene la pregunta original
    assert "cuánto tarda" not in response.lower(), "La respuesta repite la pregunta original"
    assert "buenos aires" not in response.lower() or "días" in response.lower(), "La respuesta debe incluir información de tiempo"
    assert "$" in response or "pesos" in response.lower() or "gratis" in response.lower(), "La respuesta debe mencionar el costo" 