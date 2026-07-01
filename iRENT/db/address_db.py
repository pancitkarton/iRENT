import sqlite3
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

address_folder = os.path.join(BASE_DIR, "address")
db_path = os.path.join(address_folder, "address_data.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute("""
CREATE TABLE IF NOT EXISTS regions (
    region_code TEXT PRIMARY KEY,
    region_name TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS provinces (
    province_code TEXT PRIMARY KEY,
    province_name TEXT NOT NULL,
    region_code TEXT NOT NULL,
    FOREIGN KEY (region_code)
        REFERENCES regions(region_code)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS cities (
    city_code TEXT PRIMARY KEY,
    city_name TEXT NOT NULL,
    province_code TEXT NOT NULL,
    FOREIGN KEY (province_code)
        REFERENCES provinces(province_code)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS barangays (
    brgy_code TEXT PRIMARY KEY,
    brgy_name TEXT NOT NULL,
    city_code TEXT NOT NULL,
    FOREIGN KEY (city_code)
        REFERENCES cities(city_code)
)
""")


files = [
    ("regions", "region.json"),
    ("provinces", "province.json"),
    ("cities", "city.json"),
    ("barangays", "barangay.json")
]

for table, filename in files:
    file_path = os.path.join(address_folder, filename)

    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        continue

    with open(file_path, "r", encoding="utf-8") as f:

        data = json.load(f)

        if not data:
            print(f"Warning: {filename} is empty.")
            continue

        for row in data:
            keys = ", ".join(row.keys())
            placeholders = ", ".join(["?"] * len(row))

            cursor.execute(
                f"""
                INSERT OR IGNORE INTO {table}
                ({keys})
                VALUES ({placeholders})
                """,
                tuple(row.values())
            )

        print(f"Inserted {len(data)} rows into {table}.")

conn.commit()
conn.close()