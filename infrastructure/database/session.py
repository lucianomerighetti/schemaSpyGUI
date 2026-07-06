# session.py

from sqlalchemy.orm import sessionmaker

from infrastructure.database import (
    engine
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)