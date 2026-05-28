import tkinter as tk
from tkinter import messagebox
import os
import sqlite3


#DB CREATION
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "iRENT.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Staff (
    StaffID INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName TEXT NOT NULL,
    MiddleName TEXT,
    LastName TEXT NOT NULL,
    ContactNo TEXT NOT NULL UNIQUE,
    EmailAdd TEXT NOT NULL UNIQUE,
    Username TEXT NOT NULL UNIQUE,
    Password TEXT NOT NULL
)
""")
conn.commit()



#TKINTER GUI
class iRENT:
    def __init__(self, root):
        self.root = root
        self.root.title("iRENT")
        self.root.state("zoomed")
        
        # Main container
        main_frame = tk.Frame(root)
        main_frame.pack(fill="both", expand=True)       
        
        # Left frame (60%)
        self.left_frame = tk.Frame(main_frame, bg="#ffd735", width=700)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=0, pady=0)
        self.left_frame.pack_propagate(False)  # Prevent shrinking
        
        # Right frame (40%)
        self.right_frame = tk.Frame(main_frame, bg="#313338", width=400)
        self.right_frame.pack(side="right", fill="both", expand=True)
        self.right_frame.pack_propagate(False)
        
        # Design the left side (Logo); calling function
        self.setup_logo_section()
        
        # Design the right side (Login form); calling function
        self.setup_login_section()
    


    #LOGO
    def setup_logo_section(self):
        logo = tk.PhotoImage(file="iRENT/assets/iRENT_logo.png")
        logo = logo.subsample(3,3)

        logo_label = tk.Label(
            self.left_frame, 
            fg="white",
            image = logo,
            bg="#ffd735"
        )

        logo_label.image = logo
        logo_label.pack(expand=True)
    


    #LOG-IN SECTION (RIGHT SIDE)
    def setup_login_section(self):
        # centers form in right frame
        form_frame = tk.Frame(self.right_frame, bg="#313338")
        form_frame.pack(expand=True)
        
        # Title
        tk.Label(
            form_frame, 
            text="Welcome Back!", 
            font=("Arial", 24, "bold"),
            fg="#ffd735",
            bg="#313338"
        ).pack(pady=(0, 20))
        
        # Username
        tk.Label(
            form_frame, 
            text="Username", 
            font=("Arial", 10, "bold"),
            bg="#313338",
            fg="#FFFFFF",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.username_entry = tk.Entry(
            form_frame,
            font=("Arial", 12),
            bg="#313338",
            fg="#FFFFFF",
            relief="solid",
            bd=0,
            highlightbackground="#ffd735",
            highlightcolor="#ffd735",
            highlightthickness=2
        )
        self.username_entry.pack(fill="x", pady=(0, 15), ipady=8)
        
        # Password
        tk.Label(
            form_frame, 
            text="Password", 
            font=("Arial", 10, "bold"),
            bg="#313338",
            fg="#FFFFFF",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.password_entry = tk.Entry(
            form_frame,
            font=("Arial", 12),
            bg="#313338",
            fg="#FFFFFF",
            bd=0,
            highlightbackground="#ffd735",
            highlightcolor="#ffd735",
            highlightthickness=2,
            show="*"
        )
        self.password_entry.pack(fill="x", pady=(0, 20), ipady=8)
        
        #LOG-IN BUTTON
        login_btn = tk.Button(
            form_frame,
            text="LOG IN",
            font=("Arial", 12, "bold"),
            bg="#ffd735",
            fg="black",
            relief="flat",
            cursor="hand2",
            command=self.login
        )
        login_btn.pack(fill="x", pady=(0, 20), ipady=8)
        
        links_frame = tk.Frame(form_frame, bg="#313338")
        links_frame.pack(fill="x", pady=(10, 0))
        
        def on_enter(e):
            login_btn.config(fg="#ffd735", bg="#232624")

        def on_leave(e):
            login_btn.config(fg="black", bg="#ffd735")

        login_btn.bind("<Enter>", on_enter)
        login_btn.bind("<Leave>", on_leave)



        tk.Label(
            links_frame,
            text="Don't have an account yet?",
            font=("Arial", 10),
            bg="#313338",
            fg="#7F7F7F",
        ).pack(side="left")
        
        # CREATE ACC
        create_btn = tk.Label(
            links_frame,
            text="Create an account",
            font=("Arial", 10, "underline"),
            bg="#313338",
            fg="#ffd735",
            cursor="hand2"
        )
        create_btn.pack(side="right")
        create_btn.bind("<Button-1>", lambda e: self.open_signup_window())
    



    #LOG-IN FUNCTION
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showwarning("Error", "Please enter username and password")
            return
        
        # sa mga ganito ginamit gawa nyo
        cursor.execute("SELECT * FROM Staff WHERE Username = ? AND Password = ?", (username, password))
        result = cursor.fetchone() #retrieves the username and password from the database, and checks if they match with the input

        if result:
            messagebox.showinfo("Login successful.", f"Welcome {username}!")

        #then function na ioopen ung main app pero wala pa tayo dun e

        # wrong pass
        else:
            messagebox.showwarning("Error", "Invalid username or password. Try again!")
    



    # SIGN-UP WINDOW
    def open_signup_window(self):
        signup_window = tk.Toplevel(self.root)
        signup_window.title("Create iRENT Account")
        signup_window.state("zoomed")
        signup_window.configure(bg="#313338")

        form_frame = tk.Frame(signup_window, bg="#313338")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        signup_label = tk.Label(
            form_frame, 
            text="Create an Account",
            font = ("Helvetica", 24, "bold"),
            fg= "#ffd735",
            bg = "#313338"
            ).pack(pady = 20)

        # Username
        tk.Label(
            form_frame, 
            text="Choose a Username", 
            font=("Arial", 10, "bold"),
            bg="#313338",
            fg="#FFFFFF",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        create_username = tk.Entry(
            form_frame,
            font=("Arial", 12),
            bg="#313338",
            fg="#FFFFFF",
            relief="solid",
            bd=0,
            highlightbackground="#ffd735",
            highlightcolor="#ffd735",
            highlightthickness=2
        )
        create_username.pack(fill="x", pady=(0, 15), ipady=8)

        # Password
        tk.Label(
            form_frame, 
            text="Create Password", 
            font=("Arial", 10, "bold"),
            bg="#313338",
            fg="#FFFFFF",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        create_password = tk.Entry(
            form_frame,
            font=("Arial", 12),
            bg="#313338",
            fg="#FFFFFF",
            bd=0,
            highlightbackground="#ffd735",
            highlightcolor="#ffd735",
            highlightthickness=2,
            show="*"
        )
        create_password.pack(fill="x", pady=(0, 20), ipady=8)


        # Confirm Password
        tk.Label(
            form_frame, 
            text="Confirm Password", 
            font=("Arial", 10, "bold"),
            bg="#313338",
            fg="#FFFFFF",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        confirm_password = tk.Entry(
            form_frame,
            font=("Arial", 12),
            bg="#313338",
            fg="#FFFFFF",
            bd=0,
            highlightbackground="#ffd735",
            highlightcolor="#ffd735",
            highlightthickness=2,
            show="*"
        )
        confirm_password.pack(fill="x", pady=(0, 20), ipady=8)

        # Name frame para sa first and last name
        name_frame = tk.Frame(form_frame, bg="#313338")
        name_frame.pack(fill="x", pady=(0, 15))

        #First Name
        tk.Label(
            name_frame,
            text="First Name",
            font=("Arial", 10, "bold"),
            bg="#313338",
            fg="#FFFFFF",
            anchor="w"
        ).grid(row=0, column=0, sticky="w", padx=(0, 10))

        create_firstname = tk.Entry(
            name_frame,
            font=("Arial", 12),
            bg="#313338",
            fg="#FFFFFF",
            relief="solid",
            bd=0,
            highlightbackground="#ffd735",
            highlightcolor="#ffd735",
            highlightthickness=2
        )

        create_firstname.grid(row=1, column=0, padx=(0, 10), ipady=8)

        # Last Name
        tk.Label(
            name_frame,
            text="Last Name",
            font=("Arial", 10, "bold"),
            bg="#313338",
            fg="#FFFFFF",
            anchor="w"
        ).grid(row=0, column=1, sticky="w")

        create_lastname = tk.Entry(
            name_frame,
            font=("Arial", 12),
            bg="#313338",
            fg="#FFFFFF",
            relief="solid",
            bd=0,
            highlightbackground="#ffd735",
            highlightcolor="#ffd735",
            highlightthickness=2
        )

        create_lastname.grid(row=1, column=1, ipady=8)


         # Email
        tk.Label(
            form_frame, 
            text="Email Address", 
            font=("Arial", 10, "bold"),
            bg="#313338",
            fg="#FFFFFF",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        create_email = tk.Entry(
            form_frame,
            font=("Arial", 12),
            bg="#313338",
            fg="#FFFFFF",
            relief="solid",
            bd=0,
            highlightbackground="#ffd735",
            highlightcolor="#ffd735",
            highlightthickness=2
        )
        create_email.pack(fill="x", pady=(0, 15), ipady=8)

         # Contact Number
        tk.Label(
            form_frame, 
            text="Contact Number", 
            font=("Arial", 10, "bold"),
            bg="#313338",
            fg="#FFFFFF",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        create_contact = tk.Entry(
            form_frame,
            font=("Arial", 12),
            bg="#313338",
            fg="#FFFFFF",
            relief="solid",
            bd=0,
            highlightbackground="#ffd735",
            highlightcolor="#ffd735",
            highlightthickness=2
        )
        create_contact.pack(fill="x", pady=(0, 15), ipady=8)
        

        # SIGN-UP FUNCTION
        def signup():
                first_name = create_firstname.get()     # first_name
                middle_name = ""                        # middle_name
                last_name = create_lastname.get()     # last_name
                contact_no = create_contact.get()      # contact_no
                email_add = create_email.get()        # email_add
                staff_role = "Staff"                   # staff_role
                username = create_username.get()    # username
                password = create_password.get()      # password
                confirm  =confirm_password.get()     # confirm


                if not username or not password:
                    messagebox.showwarning(
                        "Error",
                        "Please fill all fields"
                    )
                    return

                # Password mismatch
                if password != confirm:
                    messagebox.showwarning(
                        "Error",
                        "Passwords do not match."
                    )
                    return

                # Username exists
                cursor.execute(
                    "SELECT * FROM Staff WHERE Username = ?",
                    (username,)
                )

                if cursor.fetchone():
                    messagebox.showerror(
                        "Error",
                        "Username already exists!"
                    )
                    return

                # Contact exists
                cursor.execute(
                    "SELECT * FROM Staff WHERE ContactNo = ?",
                    (contact_no,)
                )

                if cursor.fetchone():
                    messagebox.showerror(
                        "Error",
                        "Contact number already exists."
                    )
                    return

                # Email exists
                cursor.execute(
                    "SELECT * FROM Staff WHERE EmailAdd = ?",
                    (email_add,)
                )

                if cursor.fetchone():
                    messagebox.showerror(
                        "Error",
                        "Email already exists."
                    )
                    return

                # INSERT INTO DATABASE
                cursor.execute("""
                    INSERT INTO Staff
                    (
                        FirstName,
                        MiddleName,
                        LastName,
                        ContactNo,
                        EmailAdd,
                        Username,
                        Password
                    )

                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    first_name,
                    middle_name,
                    last_name,
                    contact_no,
                    email_add,
                    username,
                    password
                ))

                conn.commit()

                messagebox.showinfo(
                    "Success",
                    "Sign-up successful!"
                )

                signup_window.destroy()

        # SIGN-UP BUTTON
        signup_btn = tk.Button(
            form_frame,
            text="CREATE ACCOUNT",
            font=("Arial", 12, "bold"),
            bg="#ffd735",
            fg="black",
            relief="flat",
            cursor="hand2",
            command=signup
        )
        signup_btn.pack(fill="x", pady=(0, 20), ipady=8)

        def on_enter(e):
            signup_btn.config(fg="#ffd735", bg="#232624")

        def on_leave(e):
            signup_btn.config(fg="black", bg="#ffd735")

        signup_btn.bind("<Enter>", on_enter)
        signup_btn.bind("<Leave>", on_leave)
                


# Run app
if __name__ == "__main__":
    root = tk.Tk()
    app = iRENT(root)
    root.mainloop()

conn.close()
