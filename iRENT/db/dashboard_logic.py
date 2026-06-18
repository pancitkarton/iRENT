from db.database import get_connection

def get_dashboard_summary():
    conn = get_connection()
    cursor = conn.cursor()
    
    def count(table, condition="1=1"):
        cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {condition}")
        return cursor.fetchone()[0]

    data = {
        "active": count("Rental", "RentalStatus = 'Ongoing'"),
        "overdue": count("Rental", "RentalStatus = 'Overdue'"),
        "available": count("Device", "AvailabilityStatus = 'Available'"),
        "total_devices": count("Device"),
        "total_rentees": count("Customer"),
        "total_employees": count("Staff")
    }
    
    conn.close()
    return data