# Task 1 - Profiling logic
users = {}

def signup():
  username = input("Create a username: ")
  if username in users:
    print("Username already exists!")
  else:
    password = input("Create a password: ")
    users[username] = password       #username must match with password, and vice versa
    confirmpassword = input("Confirm password: ")
    if confirmpassword == password:
      print("Sign-up successful!")
    else:
      print("Wrong password!")

def login():
  username = input("Enter username: ")
  password = input("Enter password: ")

  if username in users and users[username] == password:
    print("Login successful! Welcome back.")

  else:
    print("Invalid username or password.")

while True:
  choice = input("\n1. Sign Up\n2. Login\n3. Show all users\n4. Exit\n Choose an option: ")
  if choice == "1":
    signup()
  elif choice == "2":
    login()
  elif choice == "3":
    print(users)
  elif choice == "4":
    break
  else:
    print("Invalid choice.")


# Task 1.1 - Profiling database
import sqlite3

users = {}  #call this function in order to create a database and a table for login credentials

conn = sqlite3.connect("iRENT.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Login (
    Login_Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT(20) NOT NULL UNIQUE,
    Password TEXT(20) NOT NULL
)
''')
conn.commit()

def signup():
  username = input("Create Username: ")
  if username in users:
    print("Username already exists!")
  else:
    password = input("Create Password: ")
    users[username] = password
    confirmpassword = input("Confirm Password: ")

    if confirmpassword == password:
      cursor.execute("INSERT INTO Login (Username, Password) VALUES (?, ?)", (username, password)) #stores the username and password into the database
      conn.commit()
      print("Sign-up successful!")
    else:
      print("Invalid password. Try Again!")
      
def login():
  username = input("Enter Username: ")
  password = input("Enter Password: ")

  cursor.execute("SELECT * FROM Login WHERE Username = ? AND Password = ?", (username, password))
  result = cursor.fetchone() #retrieves the username and password from the database, and checks if they match with the input

  if result:
    print("Login successful. Welcome!")
  else:
    print("Invalid username or password. Try Again!")

def show_users():
  cursor.execute("SELECT Username FROM Login")
  users = cursor.fetchall()
  print("Registered Users:")
  for user in users:
    print(user[0]) #displays only stored username and password 

while True:
  choice = input("""
1. Sign Up
2. Login
3. Show all users
4. Exit

Choose an option: """)
  
  if choice == "1":
    signup()
  elif choice == "2":
    login()
  elif choice == "3":
    show_users()
  elif choice == "4":
    break

  else:
    print("Invalid choice. Try Again!")

conn.close() 


# Task 1.2 - Profiling tkinter
