import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


# Function to create a database connection
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='265254',
        database='webgui'
    )


# Function to add student to the database
def add_student():
    studentname = e2.get()
    coursename = e3.get()
    fee = e4.get()

    if not studentname or not coursename or not fee:
        messagebox.showerror("Input Error", "All fields must be filled.")
        return
   
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "INSERT INTO registration (name, course, fee) VALUES (%s, %s, %s)"
        values = (studentname, coursename, fee)
       
        cursor.execute(sql, values)
        conn.commit()
       
        messagebox.showinfo("Success", "Student record added successfully!")

        e2.delete(0, tk.END)
        e3.delete(0, tk.END)
        e4.delete(0, tk.END)

        load_students()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Failed to insert student: {err}")
    finally:
        conn.close()



# Function to update student record
def update_student():
    selected_item = student_tree.selection()
    if not selected_item:
        messagebox.showerror("Selection Error", "Please select a student to update.")
        return

    studentid = e1.get()
    studentname = e2.get()
    coursename = e3.get()
    fee = e4.get()

    if not studentname or not coursename or not fee:
        messagebox.showerror("Input Error", "All fields must be filled.")
        return

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "UPDATE registration SET name=%s, course=%s, fee=%s WHERE id=%s"
        values = (studentname, coursename, fee, studentid)
       
        cursor.execute(sql, values)
        conn.commit()
       
        messagebox.showinfo("Success", "Student record updated successfully!")

        load_students()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Failed to update student: {err}")
    finally:
        conn.close()



# Function to delete student
def delete_student():
    studentid = e1.get()

    if not studentid:
        messagebox.showerror("Selection Error", "Please select a student to delete.")
        return

    if not messagebox.askyesno("Confirm Delete", "Are you sure?"):
        return
   
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "DELETE FROM registration WHERE id=%s"
        cursor.execute(sql, (studentid,))
        conn.commit()
       
        messagebox.showinfo("Success", "Student record deleted!")

        load_students()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Failed to delete student: {err}")
    finally:
        conn.close()



# Function to load students
def load_students():
    for row in student_tree.get_children():
        student_tree.delete(row)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM registration")

    for r in cursor.fetchall():
        student_tree.insert("", "end", values=r)

    conn.close()



# ----------------- SEARCH / RELOAD FIX -----------------

def show_all_students():
    e_search.delete(0, tk.END)
    load_students()



def search_students():
    query = e_search.get()

    # If search box empty → show all
    if not query:
        load_students()
        return

    for row in student_tree.get_children():
        student_tree.delete(row)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM registration WHERE name LIKE %s OR course LIKE %s",
        (f"%{query}%", f"%{query}%")
    )

    for r in cursor.fetchall():
        student_tree.insert("", "end", values=r)

    conn.close()



# ----------------- EXPORT FEATURE -----------------

def export_csv():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM registration")

    rows = cursor.fetchall()

    import pandas as pd
    df = pd.DataFrame(rows, columns=["ID","Name","Course","Fee"])
    df.to_csv("students_export.csv", index=False)

    messagebox.showinfo("Export", "CSV Exported Successfully!")
    conn.close()



# ----------------- ADDED SELECT FUNCTION (YOU MISSED) -----------------

def on_tree_select(event):

    selected_item = student_tree.selection()

    if selected_item:
        vals = student_tree.item(selected_item)['values']

        # Populate ID (hidden)
        e1.config(state="normal")
        e1.delete(0, tk.END)
        e1.insert(0, vals[0])
        e1.config(state="disabled")

        e2.delete(0, tk.END)
        e2.insert(0, vals[1])

        e3.delete(0, tk.END)
        e3.insert(0, vals[2])

        e4.delete(0, tk.END)
        e4.insert(0, vals[3])



# ----------------- GUI PART -----------------

root = tk.Tk()

# Full Screen Window
root.state('zoomed')
root.title("Student Registration Dashboard")

style = ttk.Style()
style.theme_use("clam")

# Header
header = tk.Frame(root, bg="#34495e")
header.pack(fill="x")

tk.Label(header,
         text="🎓 STUDENT REGISTRATION DASHBOARD",
         font=("Arial", 18, "bold"),
         bg="#34495e",
         fg="white").pack(pady=14)



panel = tk.LabelFrame(root, text="Manage Student",
                      font=("Arial", 12, "bold"),
                      padx=20, pady=20)
panel.pack(fill="x", padx=20, pady=10)



tk.Label(panel, text="Student ID").grid(row=0, column=0)
tk.Label(panel, text="Name").grid(row=1, column=0)
tk.Label(panel, text="Course").grid(row=2, column=0)
tk.Label(panel, text="Fee").grid(row=3, column=0)



e1 = tk.Entry(panel, state="disabled")
e1.grid(row=0, column=1)

e2 = tk.Entry(panel)
e2.grid(row=1, column=1)

e3 = tk.Entry(panel)
e3.grid(row=2, column=1)

e4 = tk.Entry(panel)
e4.grid(row=3, column=1)



# Search Box
tk.Label(panel, text="Search").grid(row=0, column=2)
e_search = tk.Entry(panel)
e_search.grid(row=0, column=3)



# Buttons
ttk.Button(panel, text="➕ Add", command=add_student).grid(row=1, column=2)
ttk.Button(panel, text="✏ Update", command=update_student).grid(row=2, column=2)
ttk.Button(panel, text="🗑 Delete", command=delete_student).grid(row=3, column=2)

ttk.Button(panel, text="Find", command=search_students).grid(row=1, column=3)
ttk.Button(panel, text="Show All", command=show_all_students).grid(row=2, column=3)

ttk.Button(panel, text="📤 Export CSV", command=export_csv).grid(row=3, column=3)



# Treeview
cols = ("ID","Name","Course","Fee")
student_tree = ttk.Treeview(root, columns=cols, show="headings")
student_tree.pack(fill="both", expand=True, padx=20, pady=20)



for c in cols:
    student_tree.heading(c, text=c)
    student_tree.column(c, width=250)



# Bind event → now function exists
student_tree.bind("<ButtonRelease-1>", on_tree_select)



# Load records on start
load_students()

root.mainloop()
