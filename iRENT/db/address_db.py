import sqlite3
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

address_folder = os.path.join(BASE_DIR, "address")
db_path = os.path.join(address_folder, "address_data.db")


conn = sqlite3.connect(db_path)
cursor = conn.cursor()

files = [("regions", "region.json"), ("provinces", "province.json"), 
         ("cities", "city.json"), ("barangays", "barangay.json")]

for table, filename in files:
    file_path = os.path.join(address_folder, filename)
    
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        continue
        
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
        if not data:
            print(f"Warning: {filename} is empty.")
            continue
            
        cols = ", ".join(data[0].keys())
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} ({cols})")
        print(f"Table {table} created.")
        
        for row in data:
            keys = ", ".join(row.keys())
            placeholders = ", ".join(["?"] * len(row))
            cursor.execute(f"INSERT INTO {table} ({keys}) VALUES ({placeholders})", list(row.values()))
        
        print(f"Inserted {len(data)} rows into {table}.")

conn.commit()
conn.close()