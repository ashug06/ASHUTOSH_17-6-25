from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from contextlib import asynccontextmanager
from typing import AsyncGenerator

# Async SQLite DB URL
DATABASE_URL = "sqlite+aiosqlite:///./store_monitoring.db"

# Async engine setup
engine = create_async_engine(DATABASE_URL, echo=False)

# Session factory using async engine
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for ORM models
Base = declarative_base()

# Dependency to get a session in FastAPI or background task
@asynccontextmanager
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
