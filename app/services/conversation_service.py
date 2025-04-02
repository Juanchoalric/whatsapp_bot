from typing import Dict, List, Any
import time
from collections import defaultdict

class ConversationService:
    """
    Servicio para manejar el contexto de las conversaciones con los usuarios
    """
    
    def __init__(self):
        # Estructura para almacenar conversaciones por usuario
        # {user_id: [{"role": "user/bot", "content": "...", "timestamp": timestamp}]}
        self.conversations = defaultdict(list)
        # Tiempo máximo (en segundos) para considerar una conversación activa
        self.conversation_timeout = 3600  # 1 hora
    
    def add_message(self, user_id: str, message: str, role: str = "user"):
        """
        Agrega un mensaje a la conversación de un usuario
        
        Args:
            user_id: ID del usuario
            message: Contenido del mensaje
            role: "user" o "bot"
        """
        self.conversations[user_id].append({
            "role": role,
            "content": message,
            "timestamp": time.time()
        })
        
        # Limitar el historial a los últimos 10 mensajes para evitar problemas de contexto demasiado largo
        if len(self.conversations[user_id]) > 10:
            self.conversations[user_id] = self.conversations[user_id][-10:]
    
    def get_conversation_history(self, user_id: str, max_messages: int = 5) -> List[Dict[str, Any]]:
        """
        Obtiene el historial de conversación reciente con un usuario
        
        Args:
            user_id: ID del usuario
            max_messages: Número máximo de mensajes a devolver
            
        Returns:
            Lista de mensajes recientes
        """
        # Obtener todos los mensajes de la conversación
        conversation = self.conversations.get(user_id, [])
        
        # Filtrar mensajes que no hayan expirado
        current_time = time.time()
        active_conversation = [
            msg for msg in conversation 
            if current_time - msg["timestamp"] < self.conversation_timeout
        ]
        
        # Devolver los últimos max_messages
        return active_conversation[-max_messages:] if active_conversation else []
    
    def get_conversation_context(self, user_id: str, max_messages: int = 5) -> str:
        """
        Obtiene el contexto de la conversación en formato de texto
        
        Args:
            user_id: ID del usuario
            max_messages: Número máximo de mensajes para el contexto
            
        Returns:
            String con el contexto de la conversación
        """
        history = self.get_conversation_history(user_id, max_messages)
        
        if not history:
            return ""
            
        context = "Conversación reciente:\n\n"
        for msg in history:
            role = "Cliente" if msg["role"] == "user" else "Vos (dueño de la tienda)"
            context += f"{role}: {msg['content']}\n\n"
            
        return context
    
    def clear_expired_conversations(self):
        """
        Elimina las conversaciones que han expirado
        """
        current_time = time.time()
        for user_id in list(self.conversations.keys()):
            # Filtrar mensajes que no hayan expirado
            active_messages = [
                msg for msg in self.conversations[user_id] 
                if current_time - msg["timestamp"] < self.conversation_timeout
            ]
            
            if not active_messages:
                # Si no hay mensajes activos, eliminar la conversación
                del self.conversations[user_id]
            else:
                # Actualizar con solo los mensajes activos
                self.conversations[user_id] = active_messages 