from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
from app.report import report_status, report_file, trigger_report
import os

# Initialize FastAPI app
app = FastAPI()

# Health check endpoint to verify API is up
@app.get("/")
async def health():
    return {"message": "API is up and running."}

# Endpoint to trigger report generation
@app.post("/trigger_report")
async def trigger(
    store_id: str = None,
    start_time: str = None,
    end_time: str = None
):
    try:
        # Calls the async task to begin report generation
        report_id = trigger_report(store_id, start_time, end_time)
        return {"report_id": report_id}
    except Exception as e:
        # Return internal server error with details
        return JSONResponse(status_code=500, content={"detail": f"Error: {str(e)}"})

# Endpoint to check report status or download it
@app.get("/get_report")
async def get(report_id: str = Query(...)):
    status = report_status.get(report_id)

    if status == "COMPLETED":
        # If report is complete, return the CSV file
        file_path = report_file.get(report_id)
        if file_path and os.path.exists(file_path):
            return FileResponse(
                path=file_path,
                filename=f"{report_id}.csv",
                media_type="text/csv"
            )
        # File missing despite status — error
        return JSONResponse(status_code=500, content={"detail": "Report file not found."})

    elif status in ["IN_PROGRESS", "QUEUED"]:
        # If report is still being processed
        return {"status": status}

    elif status and status.startswith("FAILED"):
        # If task failed, return error
        return JSONResponse(status_code=500, content={"detail": status})

    else:
        # Unknown or invalid report_id
        return JSONResponse(status_code=404, content={"detail": "Invalid report_id"})
