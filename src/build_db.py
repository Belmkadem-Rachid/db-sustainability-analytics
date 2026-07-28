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

print("\n--- Gap to 2030 target ---")

cur = sqlite3.connect(DB_PATH).cursor()

cur.execute("SELECT renewable_pct FROM renewable_energy WHERE year = 2024")
current = cur.fetchone()[0]

cur.execute("SELECT renewable_pct FROM renewable_energy WHERE year = 2019")
baseline = cur.fetchone()[0]

target = 80
target_year = 2030
current_year = 2024

gap = target - current
years_remaining = target_year - current_year
required_rate = gap / years_remaining

actual_rate = (current - baseline) / (current_year - 2019)

print(f"Current (2024): {current}%")
print(f"Target (2030): {target}%")
print(f"Gap remaining: {round(gap, 2)} points")
print(f"Required rate: {round(required_rate, 2)} points/year")
print(f"Actual rate (2019-2024): {round(actual_rate, 2)} points/year")

if actual_rate >= required_rate:
    print("=> On track based on recent pace.")
else:
    print("=> Behind pace based on recent pace.")