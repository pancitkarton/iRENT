from db.database import get_connection

def get_dashboard_summary():
    conn = get_connection()
    cursor = conn.cursor()
    
    def count(table, condition="1=1"):
        cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {condition}")
        return cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(*) FROM (
            SELECT Model 
            FROM Device 
            GROUP BY Model 
            HAVING SUM(CASE WHEN AvailabilityStatus = 'Available' THEN 1 ELSE 0 END) = 0
        )
    """)
    out_of_stock_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM (
            SELECT Model 
            FROM Device 
            GROUP BY Model 
            HAVING SUM(CASE WHEN AvailabilityStatus = 'Available' THEN 1 ELSE 0 END) > 0
        )
    """)
    available_count = cursor.fetchone()[0]

    data = {
        "active": count("Rental", "RentalStatus = 'Ongoing'"),
        "overdue": count("Rental", "RentalStatus = 'Overdue'"),
        "available": available_count,
        "out_of_stock": out_of_stock_count,
        "total_devices": count("Device"),
        "total_rentees": count("Customer")
    }
    
    conn.close()
    return data

def welcome_staff(staff_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT FirstName FROM Staff WHERE StaffID = ?", (staff_id,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]
    return "Staff"