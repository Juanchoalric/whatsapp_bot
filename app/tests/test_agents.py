import pytest
import os
import sys
import json
from app.agents.classifier_agent import ClassifierAgent
from app.agents.sales_agent import SalesAgent
from app.agents.support_agent import SupportAgent

# Pruebas para el agente clasificador
@pytest.mark.asyncio
async def test_classifier_agent_product_inquiry():
    """Prueba la clasificación de una consulta sobre productos"""
    agent = ClassifierAgent()
    result = await agent.classify_message("Me gustaría saber más sobre el cuchillo Santoku que tienen")
    
    assert isinstance(result, dict)
    assert "type" in result
    assert "subtype" in result
    assert result["type"] == "sales"
    assert "product_mentioned" in result
    assert "Santoku" in result["product_mentioned"]

@pytest.mark.asyncio
async def test_classifier_agent_shipping_inquiry():
    """Prueba la clasificación de una consulta sobre envíos"""
    agent = ClassifierAgent()
    result = await agent.classify_message("¿Cuánto demora el envío a Buenos Aires?")
    
    assert isinstance(result, dict)
    assert "type" in result
    assert "subtype" in result
    assert result["type"] == "support"
    assert result["subtype"] == "shipping"

# Pruebas para el agente de ventas
@pytest.mark.asyncio
async def test_sales_agent_product_inquiry():
    """Prueba la respuesta a una consulta sobre productos"""
    agent = SalesAgent()
    response = await agent.handle_product_inquiry("¿Qué características tiene el cuchillo para chef?")
    
    assert isinstance(response, str)
    assert len(response) > 50  # Asegurarse de que la respuesta tenga contenido

@pytest.mark.asyncio
async def test_sales_agent_price_inquiry():
    """Prueba la respuesta a una consulta sobre precios"""
    agent = SalesAgent()
    response = await agent.handle_price_inquiry("Cuchillo Santoku")
    
    assert isinstance(response, str)
    assert len(response) > 30  # Asegurarse de que la respuesta tenga contenido

# Pruebas para el agente de soporte
@pytest.mark.asyncio
async def test_support_agent_general_inquiry():
    """Prueba la respuesta a una consulta general"""
    agent = SupportAgent()
    response = await agent.handle_general_inquiry("¿Cuáles son sus políticas de devolución?")
    
    assert isinstance(response, str)
    assert len(response) > 50  # Asegurarse de que la respuesta tenga contenido 