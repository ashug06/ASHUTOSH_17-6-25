# 🏪 Store Monitoring Backend — FastAPI

**Repo URL:**
[https://github.com/ashug06/ASHUTOSH\_17-6-25](https://github.com/ashug06/ASHUTOSH_17-6-25)

---

## ✅ Repository Overview

This repository was created as part of a backend development internship assignment. It implements a FastAPI-based service for monitoring the uptime and downtime of retail stores.

### Contents:

* All assignment code: `ingest.py`, `status.py`, `report.py`, `create_db.py`
* Properly named repository: `ASHUTOSH_17-6-25`
* Output CSV: `store_report.csv` (present in the repo root)
* Ideas for improvement (see below)

---

## 📂 Folder Structure

```
store_monitoring/
├── alembic/
├── app/
├── data/
├── env/
├── store_report.csv
├── ingest.py
├── status.py
├── report.py
├── create_db.py
├── requirements.txt
├── alembic.ini
├── .gitignore
└── README.md
```

---

## 🚀 Setup & Execution

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Create the DB schema**

   ```bash
   python create_db.py
   ```

3. **Ingest CSV data**

   ```bash
   python ingest.py
   ```

4. **Run the FastAPI server**

   ```bash
   uvicorn status:app --reload
   ```

5. **Trigger Report**

   ```http
   POST http://127.0.0.1:8000/trigger_report
   ```

6. **Fetch Report**

   ```http
   GET http://127.0.0.1:8000/get_report?report_id=<your_report_id>
   ```

---

## 📄 Sample Output

* `store_report.csv` file is present in the root directory.
* This file contains the computed uptime/downtime metrics over the last hour, last day, and last week for each store.

---

## 💡 Future Improvements

* Use background tasks or Celery for async report generation
* Add unit/integration tests using `pytest`
* Switch to PostgreSQL for better production reliability
* Add API documentation via Swagger/OpenAPI
* Add authentication (JWT-based) to secure endpoints
* Containerize with Docker for deployment


---

**Submitted by:** Ashutosh Goyal
**Date:** 17 June 2025
