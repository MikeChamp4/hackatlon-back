from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Optional


class OllamaSettings(BaseSettings):

    model_name: str = Field(default='gemma:7b', alias='MODEL_NAME')
    ollama_host: str = Field(default='http://localhost:11434', alias='OLLAMA_HOST')
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
