import sqlite3
import csv
import os

DB_PATH = "db/db_sustainability.sqlite"
CSV_PATH = "data/raw/db_kpi_historical.csv"

os.makedirs("db", exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS renewable_energy (
    year INTEGER PRIMARY KEY,
    renewable_pct REAL
)
""")

with open(CSV_PATH) as f:
    reader = csv.DictReader(f)
    for row in reader:
        cur.execute(
            "INSERT OR REPLACE INTO renewable_energy (year, renewable_pct) VALUES (?, ?)",
            (int(row["year"]), float(row["renewable_traction_power_pct"]))
        )

conn.commit()
print("Database built successfully.")

cur.execute("SELECT * FROM renewable_energy ORDER BY year")
for row in cur.fetchall():
    print(row)

conn.close()