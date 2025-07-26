import traceback
import time
from sqlalchemy import text
from config.db_settings import DbSettings
from database.connection_db import SessionManager
from models.user_model import UserModel


class AuthService():

    def __init__(self, db_settings: DbSettings):
        self.db_settings = db_settings

    def authenticate_user(self, user):
        """Authenticate user by checking username and password against database."""
        try:
            session_manager = SessionManager(self.db_settings)
            
            with session_manager.get_session() as session:
                # Consulta SQL usando text() para SQLAlchemy
                query = text("SELECT COUNT(*) FROM users WHERE username = :username AND password = :password")
                result = session.execute(query, {"username": user.username, "password": user.password})
                row = result.fetchone()
                
                # Si encuentra 1 registro, las credenciales son correctas
                if row and row[0] == 1:
                    print(f"✅ Usuario {user.username} autenticado correctamente")
                    return True
                else:
                    print(f"❌ Credenciales incorrectas para usuario {user.username}")
                    return False

        except Exception as e:
            print(f"Error during user authentication: {e}")
            traceback.print_exc()
            return False

    def encode_auth_token(self, user):
        """Generate a simple token for the user."""
        try:
            
            
            # Token simple con username y timestamp
            timestamp = int(time.time())
            token = f"token_{user.username}_{timestamp}"
            
            return token
            
        except Exception as e:
            print(f"Error generating token: {e}")
            return None