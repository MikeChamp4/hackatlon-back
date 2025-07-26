import ollama
from typing import Dict, Any
import logging
import os

from app.config.ollama_settings import OllamaSettings

logger = logging.getLogger(__name__)

class ChatService:
    
    def __init__(self, ollama_settings: OllamaSettings):
        self.ollama_settings = ollama_settings
        
    def _get_ollama_client(self):
        """Crear cliente de Ollama con la URL configurada"""
        try:
            client = ollama.Client(host=self.ollama_settings.ollama_host)
            return client
        except Exception as e:
            logger.error(f"Error creando cliente Ollama: {str(e)}")
            raise Exception(f"No se pudo conectar a Ollama en {self.ollama_settings.ollama_host}. Verifica que esté ejecutándose y accesible.")

    @staticmethod
    def send_message(query: str) -> Dict[str, Any]:
        """
        Envía un mensaje al modelo Gemma:7B y retorna la respuesta
        
        Args:
            query (str): La consulta del usuario
            
        Returns:
            Dict[str, Any]: Respuesta del modelo con metadata
        """
        try:
            service = ChatService(ollama_settings=OllamaSettings())
            
            # Verificar que el modelo esté disponible
            if not service._is_model_available():
                return {
                    "success": False,
                    "error": f"El modelo {service.ollama_settings.model_name} no está disponible. Asegúrate de que esté instalado con 'ollama pull {service.ollama_settings.model_name}'",
                    "response": None
                }
            
            # Obtener cliente de Ollama configurado
            client = service._get_ollama_client()
            
            # Realizar la consulta al modelo
            response = client.chat(
                model=service.ollama_settings.model_name,
                messages=[
                    {
                        'role': 'user',
                        'content': query
                    }
                ]
            )
            
            return {
                "success": True,
                "response": response['message']['content'],
                "model": service.ollama_settings.model_name,
                "query": query
            }
            
        except Exception as e:
            logger.error(f"Error en ChatService.send_message: {str(e)}")
            return {
                "success": False,
                "error": f"Error al comunicarse con el modelo: {str(e)}",
                "response": None
            }
    
    def _is_model_available(self) -> bool:
        """
        Verifica si el modelo Gemma:7B está disponible en Ollama
        
        Returns:
            bool: True si el modelo está disponible, False en caso contrario
        """
        try:
            client = self._get_ollama_client()
            models = client.list()
            available_models = [model['name'] for model in models.get('models', [])]
            return any(self.ollama_settings.model_name in model for model in available_models)
        except Exception as e:
            logger.error(f"Error verificando disponibilidad del modelo: {str(e)}")
            return False
    
    @staticmethod
    def get_model_info() -> Dict[str, Any]:
        """
        Obtiene información sobre el modelo actual
        
        Returns:
            Dict[str, Any]: Información del modelo
        """
        try:
            service = ChatService(ollama_settings=OllamaSettings())
            client = service._get_ollama_client()
            models = client.list()
            
            for model in models.get('models', []):
                if service.ollama_settings.model_name in model['name']:
                    return {
                        "success": True,
                        "model_info": {
                            "name": model['name'],
                            "size": model.get('size', 'Unknown'),
                            "modified_at": model.get('modified_at', 'Unknown'),
                            "host": service.ollama_settings.ollama_host
                        }
                    }
            
            return {
                "success": False,
                "error": f"Modelo {service.ollama_settings.model_name} no encontrado"
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo información del modelo: {str(e)}")
            return {
                "success": False,
                "error": f"Error obteniendo información del modelo: {str(e)}"
            }
