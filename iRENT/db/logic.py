#db and functions
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(BASE_DIR, "iRENT.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Users (
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        Username VARCHAR NOT NULL UNIQUE,
        Password VARCHAR NOT NULL,
        FirstName VARCHAR NOT NULL,
        LastName VARCHAR NOT NULL,
        HomeAddress VARCHAR NOT NULL,
        ContactNumber VARCHAR NOT NULL UNIQUE
)
""")
conn.commit()


#LOG-IN FUNCTION
def login(username, password):
        if not username or not password:
            return "empty"
        
        cursor.execute("SELECT * FROM Users WHERE Username = ? AND Password = ?", (username, password))
        result = cursor.fetchone() #retrieves the username and password from the database, and checks if they match with the input

        if result:
             return "success"
        else:
             return "fail"



#SIGN-UP FUNCTION
def signup(username,password,confirm,first_name,last_name,home_address,contact_number):

    if not username or not password:
        return "empty"

    # Check if password matches
    if password != confirm:
         return "mismatch"
    

    # Check if username exists
    cursor.execute(
        "SELECT * FROM Users WHERE Username = ?",
        (username,)
    )
    if cursor.fetchone():
        return "exists"

    #Inserts user into database
    cursor.execute(
        "INSERT INTO Users (Username, Password, FirstName, LastName, HomeAddress, ContactNumber) VALUES (?, ?, ?, ?, ?, ?)",
        (username, password, first_name, last_name, home_address, contact_number)
    )
    conn.commit()

    return "success"
