from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("sqlite:///store_data.db")

df = pd.read_sql("SELECT * FROM store_status ORDER BY timestamp_utc DESC LIMIT 10", engine)
print(df)
