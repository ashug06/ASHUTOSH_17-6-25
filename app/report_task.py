import os
import pandas as pd
import logging
from datetime import datetime
from app.report import generate_report

logging.basicConfig(level=logging.INFO)

async def run_report_task(report_id, session, reports):
    try:
        logging.info(f"[{report_id}] Starting report generation...")

        df = await generate_report(session)

        # Save to CSV
        os.makedirs("reports", exist_ok=True)
        filename = f"report_{report_id}.csv"
        filepath = os.path.join("reports", filename)

        df.to_csv(filepath, index=False)

        reports[report_id]["status"] = "Complete"
        reports[report_id]["path"] = filepath

        logging.info(f"[{report_id}] Report generated successfully at {filepath}")
    
    except Exception as e:
        logging.error(f"[{report_id}] Report generation failed: {e}")
        reports[report_id]["status"] = "Failed"
