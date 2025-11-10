# 📚 City Library Management System

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red.svg)
![Flask](https://img.shields.io/badge/Backend-Flask%20API-green.svg)
![Swagger](https://img.shields.io/badge/Docs-Swagger-yellow.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)

## 🧾 Project Overview

The **City Library Management System** is a **Python-based full-stack project** built to manage library operations efficiently.  
It combines a **Streamlit UI** for user interaction and a **Flask + Swagger API** for backend services — both using a shared **SQLite database**.

The system allows library admins to:
- Add, view, and delete books  
- Register members  
- Borrow and return books  
- Generate real-time reports and charts  
- Debug and inspect the live database  
- Access REST APIs with Swagger UI  

## 📁 Folder Structure

```
City Library Management System/
│
├── db/
│   └── library.db                # SQLite database file
│
├── library_db.py                 # DB connection + query utilities
├── library_core_oops.py          # Core OOP logic (Books, Members, Borrowing)
├── library_app_oops.py           # Streamlit web application
├── library_api.py                # Flask API with Swagger docs
│
├── requirements.txt              # Python dependencies
└── README.md                     # Documentation file (this file)
```

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/arunkkumar2207j/City-Library-Management-System.git
cd "City Library Management System"
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
source venv/Scripts/activate      # Windows
# or
source venv/bin/activate          # macOS/Linux
```

### 3️⃣ Install Requirements
```bash
pip install -r requirements.txt
```

### 4️⃣ Initialize Database
Database initializes automatically when you run the Streamlit app.  
To manually seed:
```bash
python library_core_oops.py
```

## 🚀 Running the Project

### ▶️ Run Streamlit Frontend
```bash
streamlit run library_app_oops.py
```
Open browser: [http://localhost:8501](http://localhost:8501)

### ▶️ Run Flask Swagger API
```bash
python library_api.py
```
Open Swagger docs: [http://127.0.0.1:5000/apidocs](http://127.0.0.1:5000/apidocs)

## 🧩 Key Features

| Feature | Description |
|----------|--------------|
| 📘 **Book Management** | Add, view, delete books with title, author, genre |
| 👥 **Member Management** | Register library members with contact info |
| 🔄 **Borrow & Return System** | Borrow and return books with date tracking |
| 📊 **Dashboard** | Real-time metrics, pie charts, and genre distribution |
| 📈 **Reports & Queries** | Borrowed books summary with search & filters |
| 🧩 **DB Debug Panel** | Inspect DB path, counts, and recent entries |
| 🔗 **Swagger API** | Interactive REST API documentation |
| 💾 **SQLite Persistence** | All actions saved permanently in `db/library.db` |

## 🔌 API Endpoints (Swagger)

| Endpoint | Method | Description |
|-----------|---------|-------------|
| `/books` | GET | Fetch all books |
| `/book` | POST | Add a new book |
| `/members` | GET | Get all members |
| `/member` | POST | Register a member |
| `/borrow` | POST | Borrow a book |
| `/return` | POST | Return a book |

Swagger UI is available at → [http://127.0.0.1:5000/apidocs](http://127.0.0.1:5000/apidocs)

## 🧠 Database Schema

### 🗃️ `books` Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| title | TEXT | Book title |
| author | TEXT | Author name |
| genre | TEXT | Genre |
| available | INTEGER | 1 = Available, 0 = Borrowed |
| borrower | TEXT | Member who borrowed the book |

### 🗃️ `members` Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| name | TEXT | Member name |
| age | INTEGER | Member age |
| contact_info | TEXT | Phone/Email |

### 🗃️ `borrowed_books` Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| book_id | INTEGER | FK to books.id |
| member_id | INTEGER | FK to members.id |
| borrow_date | TEXT | When borrowed |
| return_date | TEXT | When returned |

## 🔮 Future Enhancements

✅ Add authentication (JWT / Admin login)  
✅ Add due-date tracking & overdue fines  
✅ Export reports as Excel / PDF  
✅ Deploy using Streamlit Cloud + Render (free hosting)  
✅ Add email notifications for reminders  

## ⚙️ Requirements

```
streamlit
flask
flasgger
pandas
matplotlib
sqlite3 (built-in)
```

## 🧑‍💻 Author

**Arun Kamble**  
📧 arunkkumar2207j@gmail.com  
💼 Python Developer | AI Enthusiast  
🌐 *Developed as part of IITM Pravartak Python Project Practice Series*

## 🏁 License
This project is licensed under the **MIT License**.

## 💡 Acknowledgements
- [Streamlit Documentation](https://docs.streamlit.io)
- [Flasgger](https://github.com/flasgger/flasgger)
- [SQLite](https://www.sqlite.org)
- IITM Pravartak Python Labs Project Guidelines

---

⭐ **If this project helped you learn Python Full-Stack Development, give it a star on GitHub!**
