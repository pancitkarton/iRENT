import tkinter as tk
from tkinter import messagebox
from db import logic
from gui.app import MainApp
import os

#TKINTER GUI
class AuthApp:
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
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logo_path = os.path.join(BASE_DIR, "assets", "iRENT_logo.png")

        logo = tk.PhotoImage(file=logo_path)
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

        result = logic.login(username, password)

        if result == "empty":
            messagebox.showwarning("Error", "Please fill all fields.")

        # wrong pass
        elif result == "fail":
            messagebox.showwarning("Error", "Invalid username or password. Try again!")

        elif result == "success":
            messagebox.showinfo("Login successful.", f"Welcome {username}!")
            self.root.destroy()
            new_root = tk.Tk()
            app = MainApp(new_root)
            new_root.mainloop()





    # SIGN-UP WINDOW
    def open_signup_window(self):
        signup_window = tk.Toplevel(self.root)
        signup_window.title("Create iRENT Account")
        signup_window.state("zoomed")
        signup_window.configure(bg="#313338")

        form_frame = tk.Frame(signup_window, bg="#313338")
        form_frame.place(relx=0.5, rely=0.5, anchor="center", width=400)

        tk.Label(
            form_frame,
            text="Create an Account",
            font = ("Helvetica", 24, "bold"),
            fg= "#ffd735",
            bg = "#313338"
            ).pack(pady =(0,20))

        def user_fields (label_text, is_password=False):
            tk.Label(form_frame, 
                     text=label_text, 
                     font=("Arial", 10, "bold"), 
                     bg="#313338", 
                     fg="#FFFFFF", anchor="w"
            ).pack(fill="x", pady=(0, 5))

            entry = tk.Entry(
                form_frame, 
                font=("Arial", 12), 
                bg="#313338", 
                fg="#FFFFFF", 
                relief="solid", bd=0, 
                highlightbackground="#ffd735", 
                highlightcolor="#ffd735", 
                highlightthickness=2, show="*" if is_password else ""
            )
            entry.pack(fill="x", pady=(0, 15), ipady=8)
            return entry
        
        create_username = user_fields("Choose a Username")
        create_password = user_fields("Create Password", is_password=True)
        confirm_password = user_fields("Confirm Password", is_password=True)


        # Namesssssss
        name_frame = tk.Frame(form_frame, bg="#313338")
        name_frame.pack(fill="x", pady=(0, 15))

        name_frame.columnconfigure(0, weight=3) 
        name_frame.columnconfigure(1, weight=3) 
        name_frame.columnconfigure(2, weight=3)  
        name_frame.columnconfigure(3, weight=0)

        def name_fields(label_text, col, width=None):
            tk.Label(
                name_frame,
                text=label_text,
                font=("Arial", 10, "bold"),
                bg="#313338",
                fg="#FFFFFF",
                anchor="w"
            ).grid(row=0, column=col, sticky="w", padx=(2,2))

            entry = tk.Entry(
                name_frame,
                font=("Arial", 12),
                bg="#313338",
                fg="#FFFFFF",
                relief="solid",
                bd=0,
                highlightbackground="#ffd735",
                highlightcolor="#ffd735",
                highlightthickness=2,
                width=width
            )
            entry.grid(row=1, column=col, padx=(2,7), ipady=8, sticky="ew")
            return entry
        
        create_firstname = name_fields("First Name", 0)
        create_middlename = name_fields("Middle Name", 1)
        create_lastname = name_fields("Last Name", 2)
        create_suffix = name_fields("Suffix", 3, width=5)


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
            result = logic.signup(
                create_firstname.get(),     # first_name
                create_middlename.get(),    #middle name
                create_lastname.get(),  #lastname
                create_suffix.get(),      #suffix
                create_contact.get(),       # contact_no
                create_email.get(),         # email_add
                create_username.get(),      # username
                create_password.get(),      # password
                confirm_password.get(),      # confirm
            )

            if result == "empty":
                messagebox.showwarning(
                    "Error",
                    "Please fill all fields"
                )

            # Check if username exists
            elif result == "exists":
                messagebox.showerror(
                    "Error",
                    "Username already exists! Please try again."
                )

            # Check if contact exists
            elif result == "contact_exists":
                messagebox.showerror(
                    "Error",
                    "Contact number already exists."
                )

            # Check if email exists
            elif result == "email_exists":
                messagebox.showerror(
                    "Error",
                    "Email already exists."
                )

            # Check password match
            elif result == "mismatch":
                messagebox.showwarning("Error", "Passwords do not match.")


            else:
                messagebox.showinfo(
                    "Success",
                    "Sign-up successful! You may now login to your new account."
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