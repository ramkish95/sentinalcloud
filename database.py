from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# OS/System Design: We use SQLite for the demo, 
# but this URL is easily swapped for PostgreSQL in a Cloud environment.
SQLALCHEMY_DATABASE_URL = "sqlite:///./sentinel.db"

# Operating Systems: 'check_same_thread' is False to allow 
# FastAPI's async nature to work with SQLite.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)