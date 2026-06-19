import sqlite3
from db.database import get_connection

def get_all_customers():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Customer")
    rows = cursor.fetchall()
    
    colnames = [description[0] for description in cursor.description]
    customers = [dict(zip(colnames, row)) for row in rows]
    
    conn.close()
    return customers


def update_customer_db(customer_id, data_dict):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        query = """UPDATE Customer SET 
                   FirstName=?, MiddleName=?, LastName=?, Suffix=?, Birthday=?, 
                   ContactNumber=?, EmailAddress=?, Region=?, City=?, 
                   Barangay=?, Postal=?, Street=? 
                   WHERE CustomerID=?"""
        cursor.execute(query, (
            data_dict['FirstName'], data_dict['MiddleName'], data_dict['LastName'], 
            data_dict['Suffix'], data_dict['Birthday'], data_dict['ContactNumber'], 
            data_dict['EmailAddress'], data_dict['Region'], data_dict['City'], 
            data_dict['Barangay'], data_dict['Postal'], data_dict['Street'], 
            customer_id
        ))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error updating customer: {e}")
        return False
    finally:
        conn.close()