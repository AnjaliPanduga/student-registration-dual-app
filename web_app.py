import streamlit as st
import mysql.connector
import pandas as pd

# ---------- DATABASE CONNECTION ----------
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='265254',
        database='webgui'
    )

# ---------- LOAD STUDENTS ----------
def load_students():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, course, fee FROM registration")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return pd.DataFrame(rows, columns=["ID", "Name", "Course", "Fee"])

# ---------- ADD ----------
def add_student_db(name, course, fee):
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = "INSERT INTO registration (name, course, fee) VALUES (%s,%s,%s)"
    cursor.execute(sql, (name, course, fee))
    conn.commit()

    cursor.close()
    conn.close()

# ---------- UPDATE ----------
def update_student_db(studentid, name, course, fee):
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = "UPDATE registration SET name=%s, course=%s, fee=%s WHERE id=%s"
    cursor.execute(sql, (name, course, fee, studentid))
    conn.commit()

    cursor.close()
    conn.close()

# ---------- DELETE ----------
def delete_student_db(studentid):
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = "DELETE FROM registration WHERE id=%s"
    cursor.execute(sql, (studentid,))
    conn.commit()

    cursor.close()
    conn.close()

# ================= STREAMLIT UI =================

st.set_page_config(page_title="Intelligent Student Registration System", layout="wide")

st.title("🌐 Student Web System")

# ===================================================
# 1) ADD STUDENT
# ===================================================
st.subheader("➕ Add Student")

name_in = st.text_input("Name", key="add_name")
course_in = st.text_input("Course", key="add_course")
fee_in = st.text_input("Fee", key="add_fee")

if st.button("Add Record"):
    if name_in and course_in and fee_in:
        add_student_db(name_in, course_in, fee_in)
        st.success("Added!")
    else:
        st.error("Fill all fields")

# ===================================================
# 2) UPDATE STUDENT
# ===================================================
st.subheader("✏ Update Student")

uid_pf = st.text_input("Student ID", key="uid")
uname_pf = st.text_input("Name", key="un")
ucourse_pf = st.text_input("Course", key="uc")
ufee_pf = st.text_input("Fee", key="uf")

if st.button("Update Record"):
    if uid_pf and uname_pf and ucourse_pf and ufee_pf:
        update_student_db(uid_pf, uname_pf, ucourse_pf, ufee_pf)
        st.toast("Updated!")
    else:
        st.error("Enter ID and data")

# ===================================================
# 3) DELETE STUDENT
# ===================================================
st.subheader("🗑 Delete Student")

del_id = st.text_input("Student ID to Delete", key="delid")

if st.button("Delete Record"):
    if del_id:
        delete_student_db(del_id)
        st.warning("Deleted!")
        st.toast("All records will show below")
    else:
        st.error("Enter ID")

# ===================================================
# 👉 4) SHOW ALL RECORDS TABLE — AFTER DELETE BUTTON
# ===================================================

# Always reload data here
data = load_students()

st.subheader("📋 ALL STUDENT RECORDS")

# Search placed here if needed
search_query = st.text_input("Type Name or Course to filter", key="search_bottom")

if search_query:
    data = data[
        data["Name"].astype(str).str.contains(search_query, case=False) |
        data["Course"].astype(str).str.contains(search_query, case=False)
    ]

# 👉 TABLE AT BOTTOM ONLY
st.dataframe(data, use_container_width=True)

# ===================================================
# 👉 5) CSV DOWNLOAD — AFTER ALL RECORDS
# ===================================================

csv_data = data.to_csv(index=False)

st.download_button(
    label="📥 Download CSV",
    data=csv_data,
    file_name="students_web_download.csv",
    mime="text/csv"
)
