import asyncio
from sqlalchemy import text
from app.database import async_sessionmaker
from app.models import StoreStatus, StoreHours, StoreTimezone
from datetime import datetime, timedelta

async def seed_test_data():
    async with async_sessionmaker() as session:
        await session.execute(text("DELETE FROM store_status"))
        await session.execute(text("DELETE FROM store_hours"))
        await session.execute(text("DELETE FROM store_timezones"))

        session.add(StoreTimezone(store_id="store_1", timezone_str="America/Chicago"))
        session.add(StoreHours(store_id="store_1", day=0, start_time_local="09:00:00", end_time_local="17:00:00"))

        now = datetime.utcnow()
        for i in range(60):
            session.add(StoreStatus(
                store_id="store_1",
                timestamp_utc=now - timedelta(minutes=i),
                status="active" if i % 2 == 0 else "inactive"
            ))

        await session.commit()

if __name__ == "__main__":
    asyncio.run(seed_test_data())