#db and functions
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(BASE_DIR, "iRENT.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        Username TEXT(20) NOT NULL UNIQUE,
        Password TEXT(20) NOT NULL
)
''')

conn.commit()


#LOG-IN FUNCTION
def login(username, password):
        if not username or not password:
            return "empty"
        
        # sa mga ganito ginamit gawa nyo
        cursor.execute("SELECT * FROM Users WHERE Username = ? AND Password = ?", (username, password))
        result = cursor.fetchone() #retrieves the username and password from the database, and checks if they match with the input

        if result:
             return "success"
        else:
             return "fail"



#SIGN-UP FUNCTION
def signup(username,password,confirm):

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
        "INSERT INTO Users (Username, Password) VALUES (?, ?)", #stores the username and password into the database
        (username, password)
    )
    conn.commit()

    return "success"
