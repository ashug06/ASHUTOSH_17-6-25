# app/load_data.py

import os
import pandas as pd
from datetime import datetime
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal
from app.models import StoreStatus, StoreHours, StoreTimezone

logging.basicConfig(level=logging.INFO)
BATCH_SIZE = 1000

async def load_csv_data():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_dir = os.path.join(base_dir, "data")

    async with AsyncSessionLocal() as session:
        await insert_store_status(session, data_dir)
        await insert_store_hours(session, data_dir)
        await insert_store_timezone(session, data_dir)

    logging.info("✅ Finished loading all datasets.")

async def insert_store_status(session: AsyncSession, data_dir: str):
    path = os.path.join(data_dir, "store_status.csv")
    df = pd.read_csv(path)

    for i, row in enumerate(df.itertuples(index=False), 1):
        record = StoreStatus(
            store_id=row.store_id,
            timestamp_utc=pd.to_datetime(row.timestamp_utc, utc=True),
            status=row.status.strip().lower()
        )
        session.add(record)
        if i % BATCH_SIZE == 0:
            await session.commit()
            logging.info(f"Inserted {i} store_status records")
    await session.commit()

async def insert_store_hours(session: AsyncSession, data_dir: str):
    path = os.path.join(data_dir, "store_hours.csv")
    df = pd.read_csv(path)

    for i, row in enumerate(df.itertuples(index=False), 1):
        record = StoreHours(
            store_id=row.store_id,
            day=int(row.day),
            start_time_local=datetime.strptime(row.start_time_local, "%H:%M:%S").time(),
            end_time_local=datetime.strptime(row.end_time_local, "%H:%M:%S").time()
        )
        session.add(record)
        if i % BATCH_SIZE == 0:
            await session.commit()
            logging.info(f"Inserted {i} store_hours records")
    await session.commit()

async def insert_store_timezone(session: AsyncSession, data_dir: str):
    path = os.path.join(data_dir, "store_timezone.csv")
    df = pd.read_csv(path)

    for i, row in enumerate(df.itertuples(index=False), 1):
        record = StoreTimezone(
            store_id=row.store_id,
            timezone_str=row.timezone_str.strip()
        )
        session.add(record)
        if i % BATCH_SIZE == 0:
            await session.commit()
            logging.info(f"Inserted {i} store_timezone records")
    await session.commit()

if __name__ == "__main__":
    import asyncio
    asyncio.run(load_csv_data())
