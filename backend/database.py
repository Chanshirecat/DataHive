from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ----------------- Database URL -----------------
SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"  # SQLite file in project root

# ----------------- SQLAlchemy Engine -----------------
# check_same_thread=False is needed for SQLite + FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # type: ignore
)

# ----------------- Session Local -----------------
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ----------------- Base class for models -----------------
Base = declarative_base()

# ----------------- Dependency for FastAPI -----------------
def get_db():
    """
    Yield a database session for FastAPI dependency injection.
    Always use in routes like: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
