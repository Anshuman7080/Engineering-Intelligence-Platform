from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.settings import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_recycle=300,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)