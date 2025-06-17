from logging.config import fileConfig
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

from app.models import Base  # ✅ Import your models to get metadata

# Alembic Config object
config = context.config

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ✅ Use metadata from your models
target_metadata = Base.metadata

# ✅ Update this with your real DB URL or read from config.ini
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_async_engine(DATABASE_URL, echo=True)

    async with connectable.connect() as connection:
        await connection.run_sync(
            lambda sync_conn: context.configure(
                connection=sync_conn,
                target_metadata=target_metadata,
            )
        )

        await connection.run_sync(context.run_migrations)

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
