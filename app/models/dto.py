from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime, date

class DTO:

    def __init__(self):
        pass

# DTOs para Chat
class ChatRequest(BaseModel):
    """DTO para las requests del endpoint de chat"""
    query: str = Field(..., min_length=1, description="La consulta del usuario para el modelo")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "Explícame qué es la inteligencia artificial"
            }
        }

class ChatResponse(BaseModel):
    """DTO para las respuestas del endpoint de chat"""
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    response: Optional[str] = Field(None, description="La respuesta del modelo")
    model: Optional[str] = Field(None, description="El nombre del modelo utilizado")
    query: Optional[str] = Field(None, description="La consulta original del usuario")
    error: Optional[str] = Field(None, description="Mensaje de error si la operación falló")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "response": "La inteligencia artificial es...",
                "model": "gemma:7b",
                "query": "Explícame qué es la inteligencia artificial"
            }
        }

class ModelInfoResponse(BaseModel):
    """DTO para la información del modelo"""
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    model_info: Optional[dict] = Field(None, description="Información del modelo")
    error: Optional[str] = Field(None, description="Mensaje de error si la operación falló")

# DTOs para Usuarios
class UserCreateRequest(BaseModel):
    """DTO para crear un nuevo usuario"""
    username: str = Field(..., min_length=3, max_length=50, description="Nombre de usuario")
    email: str = Field(..., description="Correo electrónico del usuario")
    password: str = Field(..., min_length=6, description="Contraseña del usuario")
    birth_date: Optional[date] = Field(None, description="Fecha de nacimiento")
    sexo: Optional[str] = Field(None, max_length=1, description="Sexo del usuario (M/F)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "juan.perez",
                "email": "juan.perez@example.com",
                "password": "password123",
                "birth_date": "1990-01-15",
                "sexo": "M"
            }
        }

class UserUpdateRequest(BaseModel):
    """DTO para actualizar un usuario existente"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[str] = Field(None, description="Correo electrónico del usuario")
    password: Optional[str] = Field(None, min_length=6)
    birth_date: Optional[date] = Field(None)
    sexo: Optional[str] = Field(None, max_length=1)

class UserResponse(BaseModel):
    """DTO para la respuesta de usuario"""
    id: int = Field(..., description="ID del usuario")
    username: str = Field(..., description="Nombre de usuario")
    email: Optional[str] = Field(None, description="Correo electrónico")
    birth_date: Optional[date] = Field(None, description="Fecha de nacimiento")
    created_at: Optional[datetime] = Field(None, description="Fecha de creación")
    sexo: Optional[str] = Field(None, description="Sexo del usuario")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "marta.gomez",
                "email": "marta.gomez@example.com",
                "birth_date": "1985-06-12",
                "created_at": "2022-03-15T10:23:00",
                "sexo": "F"
            }
        }
