import asyncio
from datetime import datetime, timedelta, time
from app.database import async_session, engine
from app.models import Base, StoreStatus, StoreHours, StoreTimezone

async def seed():
    # Ensure tables are created (if not using Alembic)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        # 1. Insert timezone
        tz = StoreTimezone(store_id="store_1", timezone_str="America/Chicago")
        session.add(tz)

        # 2. Insert store hours (Monday = 0)
        hours = StoreHours(
            store_id="store_1",
            day=0,
            start_time_local=time(9, 0, 0),   # datetime.time object
            end_time_local=time(17, 0, 0)
        )
        session.add(hours)

        # 3. Insert status logs (past 2 hours)
        now = datetime.utcnow()
        for i in range(120):  # Last 120 minutes
            ts = now - timedelta(minutes=i)
            status = StoreStatus(
                store_id="store_1",
                timestamp_utc=ts,
                status="active" if i % 10 != 0 else "inactive"
            )
            session.add(status)

        await session.commit()
        print("✅ Sample data seeded successfully!")

if __name__ == "__main__":
    asyncio.run(seed())
