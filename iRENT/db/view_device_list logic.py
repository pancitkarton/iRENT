import sqlite3
import os
from db.database import get_connection 

# Delimiter used to join/split specs
SPECS_DELIMITER = "|"


# Ensure the SpecsText column exists (run once)
def _ensure_specs_column(conn):
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(Device)")
    columns = [col[1] for col in cursor.fetchall()]
    if "SpecsText" not in columns:
        cursor.execute("ALTER TABLE Device ADD COLUMN SpecsText TEXT")
        conn.commit()

# 1. Get all device categories (DeviceType names)
def get_categories(conn=None):
    if conn is None:
        conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT TypeName FROM DeviceType ORDER BY TypeName")
    return [row[0] for row in cursor.fetchall()]


# 2. Get all brand names under a given category
def get_brands(category_name, conn=None):
    if conn is None:
        conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT DISTINCT b.BrandName
        FROM Brand b
        JOIN Device d ON b.BrandID = d.BrandID
        JOIN DeviceType t ON d.DeviceTypeID = t.DeviceTypeID
        WHERE t.TypeName = ?
        ORDER BY b.BrandName
    ''', (category_name,))
    return [row[0] for row in cursor.fetchall()]


# 3. Get all models for a (category, brand) with specs, price, stock
def get_models(category_name, brand_name, conn=None):
    if conn is None:
        conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT
            d.Model,
            MIN(d.SerialNumber) AS sample_serial,
            AVG(d.RentalPrice) AS avg_price,
            COUNT(CASE WHEN d.AvailabilityStatus = 'Available' THEN 1 END) AS available_count,
            d.SpecsText
        FROM Device d
        JOIN DeviceType t ON d.DeviceTypeID = t.DeviceTypeID
        JOIN Brand b ON d.BrandID = b.BrandID
        WHERE t.TypeName = ? AND b.BrandName = ?
        GROUP BY d.Model
        ORDER BY d.Model
    ''', (category_name, brand_name))

    rows = cursor.fetchall()
    result = []
    for row in rows:
        # Split the specs string into a list; handle NULL/empty
        specs_text = row[4] or ""
        specs = specs_text.split(SPECS_DELIMITER) if specs_text else []
        result.append({
            'model_name': row[0],
            'id': row[1],                     # sample serial as product ID
            'price': int(row[2]) if row[2] else 0,
            'available': row[3] if row[3] is not None else 0,
            'specs': specs
        })
    return result

# 4. Add a new model (insert multiple devices with identical specs)
def add_model(category_name, brand_name, model_name, product_id,
              price, stock_count, specs_list, conn=None):

    if conn is None:
        conn = get_connection()
        close_conn = True
    else:
        close_conn = False

    cursor = conn.cursor()
    _ensure_specs_column(conn)

    # Get foreign keys
    cursor.execute("SELECT DeviceTypeID FROM DeviceType WHERE TypeName = ?", (category_name,))
    type_row = cursor.fetchone()
    if not type_row:
        if close_conn: conn.close()
        return False, f"Category '{category_name}' not found."
    type_id = type_row[0]

    cursor.execute("SELECT BrandID FROM Brand WHERE BrandName = ?", (brand_name,))
    brand_row = cursor.fetchone()
    if not brand_row:
        if close_conn: conn.close()
        return False, f"Brand '{brand_name}' not found."
    brand_id = brand_row[0]

    # Optional duplicate check
    cursor.execute('''
        SELECT 1 FROM Device
        WHERE Model = ? AND BrandID = ? AND DeviceTypeID = ?
        LIMIT 1
    ''', (model_name, brand_id, type_id))
    if cursor.fetchone():
        if close_conn: conn.close()
        return False, f"Model '{model_name}' already exists for this brand."

    # Join specs with delimiter
    specs_text = SPECS_DELIMITER.join(specs_list)

    # Insert each unit
    for i in range(stock_count):
        serial = f"{product_id}-{i+1:03d}"
        cursor.execute('''
            INSERT INTO Device
            (Model, SerialNumber, RentalPrice, FunctionalStatus,
             Appearance, AvailabilityStatus, DeviceTypeID, BrandID, SpecsText)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (model_name, serial, price, 'Excellent', 'New', 'Available',
              type_id, brand_id, specs_text))

    conn.commit()
    if close_conn:
        conn.close()
    return True, f"Model '{model_name}' added with {stock_count} device(s)."