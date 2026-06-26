import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "address", "address_data.db")

def addressdb():
    return sqlite3.connect(db_path)

def regionsdb():
    conn = addressdb()
    try:
        return conn.execute("SELECT region_code, region_name FROM regions").fetchall()
    finally:
        conn.close()

def provincesdb(region_code):
    conn = addressdb()
    try:
        return conn.execute("SELECT province_code, province_name FROM provinces WHERE region_code = ?", (region_code,)).fetchall()
    finally:
        conn.close()

def citiesdb(province_code):
    conn = addressdb()
    try:
        return conn.execute("SELECT city_code, city_name FROM cities WHERE province_code = ?", (province_code,)).fetchall()
    finally:
        conn.close()

def brgysdb(city_code):
    conn = addressdb()
    try:
        return conn.execute("SELECT brgy_code, brgy_name FROM barangays WHERE city_code = ?", (city_code,)).fetchall()
    finally:
        conn.close()