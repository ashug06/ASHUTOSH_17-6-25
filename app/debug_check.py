import asyncio
from typing import cast
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.database import async_session
from app.models import StoreStatus, StoreHours, StoreTimezone

async def check_counts():
    async with async_session() as session:
        session = cast(AsyncSession, session)

        store_status_count = (await session.execute(text("SELECT COUNT(*) FROM store_status"))).scalar()
        store_hours_count = (await session.execute(text("SELECT COUNT(*) FROM store_hours"))).scalar()
        timezone_count = (await session.execute(text("SELECT COUNT(*) FROM store_timezone"))).scalar()

        print(f"StoreStatus: {store_status_count} rows")
        print(f"StoreHours: {store_hours_count} rows")
        print(f"StoreTimezone: {timezone_count} rows")

if __name__ == "__main__":
    asyncio.run(check_counts())
