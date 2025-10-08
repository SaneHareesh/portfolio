import sqlite3
from tkinter import *
from tkinter import messagebox
import webbrowser
import os

DB_NAME = 'login.db'
# Define the specific path to the HTML file
HTML_PATH = 'file:///D:/Portfolio/index.html'

# --- Database Connection and Setup ---
try:
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS user(username TEXT PRIMARY KEY, password TEXT)")
    con.commit()
except sqlite3.Error as e:
    print(f"Database error: {e}")
    exit()

# --- Function to View Data (for testing) ---
def view_data():
    try:
        cur.execute("SELECT * FROM user")
        data = cur.fetchall()
        print("\n--- Current Data in 'user' Table ---")
        if data:
            for row in data:
                print(row)
        else:
            print("The table is currently empty.")
        print("--------------------------------------\n")
    except Exception as e:
        print(f"Failed to fetch data: {e}")

# --- MODIFIED Registration Function ---
def register_user():
    username = e1.get()
    password = e2.get()


    if not username or not password:
        messagebox.showerror("Error", "Username and Password cannot be empty.")
        return

    try:
        sql = "INSERT INTO user (username, password) VALUES (?, ?)"
        cur.execute(sql, (username, password))
        con.commit()
        
        messagebox.showinfo("Success", f"User '{username}' registered successfully!")
        e1.delete(0, END)
        e2.delete(0, END)
        
        # Opens page upon successful registration
        try:
            webbrowser.open_new_tab(HTML_PATH)
        except Exception as e:
            messagebox.showerror("Browser Error", f"Failed to open HTML page: {e}")
        
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", f"Username '{username}' already exists.")
        
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")


# --- Tkinter GUI Setup ---
har = Tk()
har.title("Login/Registration Form")
har.geometry("400x400")
har.config(bg="lightblue")
har.resizable(True, False)

l = Label(har, text="Registration Form", font=("times new roman", 15, "bold"), fg="blue", bg="lightgreen")
l.pack(anchor=CENTER, pady=20, padx=20)

l1 = Label(har, text="Username", font=("times new roman", 10, "bold"), fg="blue", bg="lightgreen")
l1.pack(anchor=CENTER, pady=10)
e1 = Entry(har, font=("times new roman", 10), bd=3, bg="lightgreen")
e1.pack(anchor=CENTER, pady=10)

l2 = Label(har, text="Password", font=("times new roman", 10, "bold"), fg="blue", bg="lightgreen")
l2.pack(anchor=CENTER, pady=10)
e2 = Entry(har, font=("times new roman", 10), bd=3, show="*", bg="lightgreen")
e2.pack(anchor=CENTER, pady=10)

# Register button calls the register_user function
b = Button(har, text="Register", font=("times new roman", 10, "bold"), fg="blue", bg="lightgreen", command=register_user)
b.pack(anchor=CENTER, pady=10)

# # Optional button to manually open the page
# b_html = Button(har, text="Open Portfolio Page", font=("times new roman", 10, "bold"), fg="white", bg="darkblue", command=open_html_page)
# b_html.pack(anchor=CENTER, pady=10)

view_data()

har.mainloop()

# --- Close Connection ---
cur.close()
con.close()