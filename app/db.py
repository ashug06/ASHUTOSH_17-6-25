from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Path to your SQLite database file
DATABASE_URL = "sqlite+aiosqlite:///./store.db"

# Create an async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False  # Set to True to see SQL logs
)

# Create a session factory for async sessions
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
