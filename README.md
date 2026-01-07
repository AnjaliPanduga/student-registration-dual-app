Student Registration System with Dual Interfaces using Tkinter, Streamlit & MySQL

🌟 Project Overview

This application is a complete Student Registration System built with both:

✅ A Desktop GUI using Tkinter
✅ A Web Interface using Streamlit

Both interfaces interact with a MySQL database to manage student records — allowing users to add, update, delete, search, and export student information.

This project demonstrates full CRUD operations, cross-platform UI design, and real database integration.

💡 Key Features

✔ Add student (Name, Course, Fee)
✔ Update student details
✔ Delete students
✔ Search by name or course
✔ Display all student records
✔ Export to CSV in Desktop app
✔ Download CSV in Web app
✔ Dual interface: Desktop + Web

🗃️ Project Files
student-registration-dual-app/
```
├── desktop_app.py          # Tkinter Desktop GUI Code
├── web_app.py              # Streamlit Web App Code
├── database.sql            # MySQL Database Script
├── requirements.txt        # Project Dependencies
├── screenshots/            # 📸 Application Images
│   ├── tkinter_dashboard.png
│   ├── streamlit_home.png
│   └── mysql_table.png
└── README.md               # Project Documentation

```
🚀 Tech Stack
Tool / Library	Purpose
Python	Programming Language
Tkinter	Desktop GUI Interface
Streamlit	Web Interface
MySQL	Database
mysql-connector-python	Python ↔ MySQL Connection
pandas	Data handling & CSV Export
🧠 How It Works
Desktop (Tkinter)

Opens a full GUI window.

User can Add, Edit, Delete student records.

Search functionality filters table.

Export current data to a CSV file.

Web (Streamlit)

Provides a modern web browser interface.

Adds & updates students via forms.

Shows all records with filter search.

Allows CSV file download.

💻 How to Run Locally
1️⃣ Clone the repository
```
git clone https://github.com/AnjaliPanduga/student-registration-dual-app.git
cd student-registration-dual-app
```
2️⃣ Create the database
```
Import database.sql into MySQL:
```
mysql -u root -p
SOURCE database.sql
```
3️⃣ Install Dependencies
pip install -r requirements.txt
```
4️⃣ Run the Desktop App
```
python desktop_app.py
```
5️⃣ Run the Web App
```
streamlit run web_app.py
```





`
