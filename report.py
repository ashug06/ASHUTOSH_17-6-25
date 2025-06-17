# app/report.py

import pandas as pd
import uuid
import pytz
import logging
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import StoreStatus, StoreHours, StoreTimezone

logger = logging.getLogger(__name__)

# Required for /get_report endpoint
report_status = {}   # report_id -> "pending", "complete", "failed"
report_file = {}     # report_id -> CSV string


async def generate_report(session: AsyncSession, store_id=None, start_time=None, end_time=None):
    now = datetime.utcnow()
    start = datetime.fromisoformat(start_time) if start_time else now - timedelta(days=1)
    end = datetime.fromisoformat(end_time) if end_time else now

    statuses = (await session.execute(select(StoreStatus))).scalars().all()
    hours = (await session.execute(select(StoreHours))).scalars().all()
    timezones = (await session.execute(select(StoreTimezone))).scalars().all()

    df_s = pd.DataFrame([{"store_id": s.store_id, "ts": s.timestamp_utc, "status": s.status} for s in statuses])
    df_h = pd.DataFrame([{"store_id": h.store_id, "day": h.day, "start": h.start_time_local, "end": h.end_time_local} for h in hours])
    df_t = pd.DataFrame([{"store_id": t.store_id, "tz": t.timezone_str} for t in timezones])

    if df_s.empty:
        return []

    df = df_s.merge(df_t, on="store_id", how="left")
    report = []

    for sid, group in df.groupby("store_id"):
        tz = pytz.timezone(group["tz"].iloc[0] or "UTC")
        group["ts"] = pd.to_datetime(group["ts"], utc=True)
        group["ts_local"] = group["ts"].dt.tz_convert(tz)

        rec = {"store_id": sid}
        for label, delta in {
            "last_hour": timedelta(hours=1),
            "last_day": timedelta(days=1),
            "last_week": timedelta(weeks=1)
        }.items():
            window_start = end - delta
            sl = group[(group["ts"] >= window_start) & (group["ts"] <= end)]
            up = (sl["status"] == "active").sum()
            down = (sl["status"] == "inactive").sum()
            total = up + down
            pct = (up / total * 100) if total else None
            rec[f"uptime_{label}"] = up
            rec[f"downtime_{label}"] = down
            rec[f"availability_{label}_percent"] = round(pct, 2) if pct else None

        report.append(rec)

    return report


async def _run_report_task(session_gen, report_id, store_id, start_time, end_time):
    try:
        async with session_gen() as session:
            data = await generate_report(session, store_id, start_time, end_time)
            df = pd.DataFrame(data)
            csv_data = df.to_csv(index=False)
            report_status[report_id] = "complete"
            report_file[report_id] = csv_data
    except Exception as e:
        report_status[report_id] = "failed"
        report_file[report_id] = None


def trigger_report(session_gen, store_id=None, start_time=None, end_time=None):
    report_id = str(uuid.uuid4())
    report_status[report_id] = "pending"

    import asyncio
    asyncio.create_task(_run_report_task(session_gen, report_id, store_id, start_time, end_time))

    return report_id
