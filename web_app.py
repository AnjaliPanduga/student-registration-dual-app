import streamlit as st
import pandas as pd
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Student Registration Demo",
    layout="wide"
)

st.title("🌐 Student Web System — Demo Mode (No MySQL)")

# ---------------- CSV BACKEND ----------------
CSV_FILE = "students_export.csv"


# ---------- LOAD STUDENTS ----------
def load_students():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["ID", "Name", "Course", "Fee"])



# ---------- ADD STUDENT ----------
def add_student(name, course, fee):

    df = load_students()

    new_id = len(df) + 1

    new_row = pd.DataFrame(
        [[new_id, name, course, fee]],
        columns=["ID", "Name", "Course", "Fee"]
    )

    df = pd.concat([df, new_row], ignore_index=True)

    df.to_csv(CSV_FILE, index=False)

    return df



# ---------- UPDATE STUDENT ----------
def update_student(studentid, name, course, fee):

    df = load_students()

    if studentid not in df["ID"].astype(str).values:
        st.error("ID Not Found!")
        return df

    df.loc[df["ID"].astype(str) == studentid, ["Name","Course","Fee"]] = [name, course, fee]

    df.to_csv(CSV_FILE, index=False)

    return df



# ---------- DELETE STUDENT ----------
def delete_student(studentid):

    df = load_students()

    if studentid not in df["ID"].astype(str).values:
        st.error("ID Not Found!")
        return df

    df = df[df["ID"].astype(str) != studentid]

    # Reorder IDs again
    df["ID"] = range(1, len(df) + 1)

    df.to_csv(CSV_FILE, index=False)

    return df



# ================= STREAMLIT UI =================


# ===================================================
# 1) ADD STUDENT
# ===================================================
st.subheader("➕ Add Student")

name_in = st.text_input("Name", key="add_name")
course_in = st.text_input("Course", key="add_course")
fee_in = st.text_input("Fee", key="add_fee")

if st.button("Add Record"):

    if name_in and course_in and fee_in:
        add_student(name_in, course_in, fee_in)
        st.success("Added Successfully!")
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
        update_student(uid_pf, uname_pf, ucourse_pf, ufee_pf)
        st.toast("Updated Successfully!")
    else:
        st.error("Enter ID and data")



# ===================================================
# 3) DELETE STUDENT
# ===================================================
st.subheader("🗑 Delete Student")

del_id = st.text_input("Student ID to Delete", key="delid")

if st.button("Delete Record"):

    if del_id:
        delete_student(del_id)
        st.warning("Deleted!")
        st.toast("Table reloaded")
    else:
        st.error("Enter ID")



# ===================================================
# 4) SHOW ALL RECORDS — AT BOTTOM
# ===================================================

data = load_students()

st.subheader("📋 ALL STUDENT RECORDS")

search_query = st.text_input("Search by Name or Course", key="search_bottom")

if search_query:
    data = data[
        data["Name"].astype(str).str.contains(search_query, case=False) |
        data["Course"].astype(str).str.contains(search_query, case=False)
    ]


st.dataframe(data, use_container_width=True)



# ===================================================
# 5) CSV DOWNLOAD
# ===================================================

csv_data = data.to_csv(index=False)

st.download_button(
    label="📥 Download CSV",
    data=csv_data,
    file_name="students_web_download.csv",
    mime="text/csv"
)


# ---------- INITIAL EMPTY FILE CHECK ----------
if not os.path.exists(CSV_FILE):
    init_df = pd.DataFrame(columns=["ID","Name","Course","Fee"])
    init_df.to_csv(CSV_FILE, index=False)
