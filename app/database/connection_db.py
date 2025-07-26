from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from config.db_settings import DbSettings


class SessionManager:

    def __init__(self, db_settings: DbSettings):
        self.engine = create_engine(db_settings.database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    @contextmanager
    def get_session(self, session: Session = None) -> Generator[Session, None, None]:
        """Provide a transactional scope around a series of operations."""
        is_external = session is not None
        session = session or self.SessionLocal()
        try:
            yield session
            if not is_external:
                session.commit()
        except Exception as e:
            print(f"Error in DB session: {e}")
            session.rollback()
            raise
        finally:
            if not is_external:
                session.close()
