import os
from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Optional


class DbSettings(BaseSettings):
    
    db_host: str = Field(default='localhost', alias='DB_HOST')
    db_port: str = Field(default='3306', alias='DB_PORT')
    db_name: str = Field(default='techtalent_db', alias='DB_NAME')
    db_username: str = Field(default='root', alias='DB_USERNAME')
    db_password: str = Field(default='', alias='DB_PASSWORD')


    # db_host: str = os.getenv('DB_HOST', 'localhost')
    # db_port: str = os.getenv('DB_PORT', '3306')
    # db_name: str = os.getenv('DB_NAME', 'techtalent_db')
    # db_username: str = os.getenv('DB_USERNAME', 'root')
    # db_password: str = os.getenv('DB_PASSWORD', '')
    
    secret_key: Optional[str] = Field(default=None, alias='SECRET_KEY')
    flask_debug: Optional[str] = Field(default=None, alias='FLASK_DEBUG')

    secret_key: str = os.getenv('SECRET_KEY', 'default_secret_key')
    flask_debug: str = os.getenv('FLASK_DEBUG', 'False')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

    @property
    def database_url(self) -> str:
        """Genera la URL de conexión a MySQL a partir de los campos."""
        return f"mysql+pymysql://{self.db_username}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
