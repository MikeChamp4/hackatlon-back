import os
from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Optional


class DbSettings(BaseSettings):
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}
    
    db_host: str = Field(default='localhost', alias='DB_HOST')
    db_port: str = Field(default='3306', alias='DB_PORT')
    db_name: str = Field(default='techtalent_db', alias='DB_NAME')
    db_username: str = Field(default='root', alias='DB_USERNAME')
    db_password: str = Field(default='', alias='DB_PASSWORD')
    
    # Optional fields for future use
    secret_key: Optional[str] = Field(default=None, alias='SECRET_KEY')
    flask_debug: Optional[str] = Field(default=None, alias='FLASK_DEBUG')

    @property
    def database_url(self) -> str:
        """Genera la URL de conexión a MySQL a partir de los campos."""
        return f"mysql+pymysql://{self.db_username}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
