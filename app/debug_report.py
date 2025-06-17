import asyncio
from app.database import async_session
from app.report import generate_report

async def run_report():
    async with async_session() as session:
        df = await generate_report(session)
        print(df.head())

if __name__ == "__main__":
    asyncio.run(run_report())
