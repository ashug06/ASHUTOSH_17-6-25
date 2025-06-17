import pandas as pd
import sqlite3

# Connect to SQLite database (or create it)
conn = sqlite3.connect('store_data.db')

# Load CSV files
df_status = pd.read_csv('data/store_status.csv')
df_hours = pd.read_csv('data/store_hours.csv')
df_zones = pd.read_csv('data/store_timezone.csv')


# Save to SQL tables
df_status.to_sql('store_status', conn, if_exists='replace', index=False)
print("✅ store_status imported")

df_hours.to_sql('store_hours', conn, if_exists='replace', index=False)
print("✅ store_hours imported")

df_zones.to_sql('store_timezone', conn, if_exists='replace', index=False)
print("✅ store_timezone imported")

# Close the connection
conn.close()
