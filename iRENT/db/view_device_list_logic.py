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

    # Also ensure Functionality column exists
    if "Functionality" not in columns:
        cursor.execute("ALTER TABLE Device ADD COLUMN Functionality TEXT DEFAULT 'Excellent'")
        conn.commit()

    if "ProductID" not in columns:
        cursor.execute("ALTER TABLE Device ADD COLUMN ProductID TEXT")
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


# 3. Get all models for a (category, brand) with specs, price, stock, functionality, serial_num
def get_models(category_name, brand_name, conn=None):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT
            d.Model,
            d.ProductID AS product_id,
            MIN(d.SerialNumber) AS sample_serial,
            AVG(d.RentalPrice) AS avg_price,
            COUNT(CASE WHEN d.AvailabilityStatus = 'Available' THEN 1 END) AS available_count,
            d.SpecsText,
            d.Functionality,
            d.SerialNumber
        FROM Device d
        JOIN DeviceType t ON d.DeviceTypeID = t.DeviceTypeID
        JOIN Brand b ON d.BrandID = b.BrandID
        WHERE t.TypeName = ? AND b.BrandName = ?
        GROUP BY d.Model
    ''', (category_name, brand_name))

    # Return:
    result = []
    rows = cursor.fetchall()
    for row in rows:
        # Split the specs string into a list; handle NULL/empty
        specs_text = row[5] or ""
        specs = specs_text.split(SPECS_DELIMITER) if specs_text else []
        result.append({
            'model_name': row[0],
            'id': row[1],                                        # Product ID
            'price': int(row[3]) if row[3] else 0,               # Price
            'available': row[4] if row[4] is not None else 0,    # Count
            'specs': specs,
            'functionality': row[6] if row[6] else 'Excellent',  # Functionality
            'serial_num': row[2] if row[2] else 'N/A'            # Serial
        })
    return result


# 4. Add a new model (insert multiple devices with identical specs)
def add_model(category_name, brand_name, model_name, product_id,
              price, stock_count, specs_list, functionality='Excellent',
              serial_num='N/A', conn=None):

    # Get foreign keys
    if conn is None:
        conn = get_connection()
        close_conn = True
    else:
        close_conn = False
        cursor = conn.cursor()

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
        serial = f"{serial_num}-{i+1:03d}"
        cursor.execute('''
            INSERT INTO Device
            (Model, ProductID, SerialNumber, RentalPrice, FunctionalStatus,
             Appearance, AvailabilityStatus, DeviceTypeID, BrandID, SpecsText, Functionality)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (model_name, product_id, serial, price, functionality, 'New', 'Available', type_id, brand_id, specs_text, functionality))

    conn.commit()
    if close_conn:
        conn.close()
    return True, f"Model '{model_name}' added with {stock_count} device(s)."


# 5. Delete a model from the database
def delete_model(category_name, brand_name, model_name, conn=None):
    """Delete all devices matching the model name under a specific brand and category"""

    if conn is None:
        conn = get_connection()
        close_conn = True
    else:
        close_conn = False

    cursor = conn.cursor()

    try:
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

        # Check if model exists
        cursor.execute('''
            SELECT COUNT(*) FROM Device
            WHERE Model = ? AND BrandID = ? AND DeviceTypeID = ?
        ''', (model_name, brand_id, type_id))
        count = cursor.fetchone()[0]

        if count == 0:
            if close_conn: conn.close()
            return False, f"Model '{model_name}' not found."

        # Delete all devices with this model
        cursor.execute('''
            DELETE FROM Device
            WHERE Model = ? AND BrandID = ? AND DeviceTypeID = ?
        ''', (model_name, brand_id, type_id))

        conn.commit()
        if close_conn:
            conn.close()
        return True, f"Model '{model_name}' deleted successfully! ({count} device(s) removed)"

    except Exception as e:
        if close_conn:
            conn.close()
        return False, f"Error deleting model: {str(e)}"


# 6. Update model details in the database
def update_model(category_name, brand_name, model_name, new_model_name,
                 new_id, new_serial, new_functionality, new_specs,
                 new_price, conn=None):

    if conn is None:
        conn = get_connection()
        close_conn = True
    else:
        close_conn = False

    cursor = conn.cursor()

    try:
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

        # Check if model exists
        cursor.execute('''
            SELECT COUNT(*) FROM Device
            WHERE Model = ? AND BrandID = ? AND DeviceTypeID = ?
        ''', (model_name, brand_id, type_id))
        count = cursor.fetchone()[0]

        if count == 0:
            if close_conn: conn.close()
            return False, f"Model '{model_name}' not found."

        # If model name changed, check for duplicates
        if new_model_name != model_name:
            cursor.execute('''
                SELECT 1 FROM Device
                WHERE Model = ? AND BrandID = ? AND DeviceTypeID = ?
                LIMIT 1
            ''', (new_model_name, brand_id, type_id))
            if cursor.fetchone():
                if close_conn: conn.close()
                return False, f"Model '{new_model_name}' already exists for this brand."

        # Join specs with delimiter
        specs_text = SPECS_DELIMITER.join(new_specs)

        # Get the first device's serial to update sample
        cursor.execute('''
            SELECT DeviceID FROM Device
            WHERE Model = ? AND BrandID = ? AND DeviceTypeID = ?
            LIMIT 1
        ''', (model_name, brand_id, type_id))
        device_id = cursor.fetchone()[0]

        # Update the model name, price, specs, and functionality for all devices
        cursor.execute('''
            UPDATE Device
            SET Model = ?,
                ProductID = ?,
                RentalPrice = ?,
                SpecsText = ?,
                Functionality = ?
            WHERE Model = ? AND BrandID = ? AND DeviceTypeID = ?
        ''', (new_model_name, new_id, new_price, specs_text, new_functionality,
              model_name, brand_id, type_id))

        # Also update the serial number for the first device (as sample)
        cursor.execute('''
            UPDATE Device
            SET SerialNumber = ?
            WHERE DeviceID = ?
        ''', (new_serial, device_id))

        conn.commit()
        if close_conn:
            conn.close()
        return True, f"Model '{model_name}' updated successfully!"

    except Exception as e:
        if close_conn:
            conn.close()
        return False, f"Error updating model: {str(e)}"