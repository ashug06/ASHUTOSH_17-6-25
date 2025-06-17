import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import StoreStatus, StoreHours, StoreTimezone
import pytz
import uuid
import os
import csv
import asyncio

from app.database import async_session

# Dictionary to track the status of report generation by report_id
report_status = {}

# Dictionary to track the generated report file path by report_id
report_file = {}

# Generates a CSV report for uptime/downtime metrics for a store or all stores
async def generate_report(session: AsyncSession, store_id=None, start_time=None, end_time=None):
    now = datetime.utcnow()

    # Parse and validate time range inputs
    try:
        start = datetime.fromisoformat(start_time) if start_time else now - timedelta(days=1)
        end = datetime.fromisoformat(end_time) if end_time else now
    except Exception:
        raise ValueError("start_time/end_time must be ISO format, e.g., 'YYYY-MM-DDTHH:MM:SS'")

    # Fetch data from DB
    q = select(StoreStatus)
    if store_id:
        q = q.where(StoreStatus.store_id == store_id)
    statuses = (await session.execute(q)).scalars().all()
    hours = (await session.execute(select(StoreHours))).scalars().all()
    timezones = (await session.execute(select(StoreTimezone))).scalars().all()

    # Convert to DataFrames for processing
    df_s = pd.DataFrame([{"store_id": s.store_id, "ts": s.timestamp_utc, "status": s.status} for s in statuses])
    df_h = pd.DataFrame([{"store_id": h.store_id, "day": h.day, "start": h.start_time_local, "end": h.end_time_local} for h in hours])
    df_t = pd.DataFrame([{"store_id": t.store_id, "tz": t.timezone_str} for t in timezones])

    if df_s.empty:
        return []  # No status data, return early

    # Merge status with timezone info
    df = df_s.merge(df_t, on="store_id", how="left")

    # Define time windows for analysis
    time_windows = {
        "last_hour": end - timedelta(hours=1),
        "last_day": end - timedelta(days=1),
        "last_week": end - timedelta(weeks=1)
    }

    report = []

    # Group by store and compute metrics
    for sid, group in df.groupby("store_id"):
        tz_str = group["tz"].iloc[0]
        if not isinstance(tz_str, str):  # fallback for missing timezone
            tz_str = "UTC"
        tz = pytz.timezone(tz_str)

        # Convert UTC timestamps to local time
        group["ts_local"] = pd.to_datetime(group["ts"]).dt.tz_localize("UTC").dt.tz_convert(tz)

        rec = {"store_id": sid}
        filtered = group[(group["ts"] >= start) & (group["ts"] <= end)]

        # Calculate uptime/downtime for each time window
        for label in ["last_hour", "last_day", "last_week"]:
            sl = filtered[filtered["ts"] >= time_windows[label]]
            up = (sl["status"] == "active").sum()
            down = (sl["status"] == "inactive").sum()
            total = up + down
            pct = (up / total * 100) if total else None  # Avoid divide by zero
            rec[f"uptime_{label}"] = up
            rec[f"downtime_{label}"] = down
            rec[f"availability_{label}_percent"] = round(pct, 2) if pct is not None else None

        report.append(rec)

    return report

# Runs the report generation in background and stores result to CSV
async def process_report_task(report_id: str, store_id=None, start_time=None, end_time=None):
    try:
        report_status[report_id] = "IN_PROGRESS"
        async with async_session() as session:
            df = await generate_report(session, store_id, start_time, end_time)

        # Save report to CSV file
        filepath = f"generated_reports/report_{report_id}.csv"
        os.makedirs("generated_reports", exist_ok=True)

        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=df[0].keys())
            writer.writeheader()
            writer.writerows(df)

        report_file[report_id] = filepath
        report_status[report_id] = "COMPLETED"

    except Exception as e:
        # If an error occurs, print traceback and mark report as failed
        import traceback
        print(traceback.format_exc())
        report_status[report_id] = f"FAILED: {str(e)}"

# External API call triggers this to start report generation task
def trigger_report(store_id=None, start_time=None, end_time=None):
    report_id = str(uuid.uuid4())  # Generate unique ID for the report

    # Define async task wrapper
    async def task():
        await process_report_task(report_id, store_id, start_time, end_time)

    # Schedule task in event loop
    asyncio.create_task(task())
    report_status[report_id] = "QUEUED"
    return report_id
