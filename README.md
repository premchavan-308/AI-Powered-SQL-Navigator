# 📊 AI-Powered Natural Language to SQL Query Navigator

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![LLM Engine](https://img.shields.io/badge/LLM-Gemini%201.5%20Flash-orange.svg)](https://deepmind.google/technologies/gemini/)
[![Database](https://img.shields.io/badge/Database-MySQL-4479A1.svg)](https://www.mysql.com/)

An AI-powered web application that allows users to query a MySQL database using natural language. The system converts user questions into SQL queries using Google's Gemini API, executes the generated query on a MySQL database, and displays the results through an interactive Streamlit interface.

## 🚀 Project Overview

Many users are unfamiliar with SQL syntax but still need to retrieve information from databases. This project bridges that gap by enabling users to interact with databases using plain English.

### Example

**User Input:**

```text
Show all employees
```

**Generated SQL:**

```sql
SELECT * FROM employees;
```

The application executes the query and displays the results in a tabular format.

---

# 🏗️ System Architecture

```text
User Query
     │
     ▼
Streamlit Frontend
     │
     ▼
Gemini API
(Natural Language → SQL)
     │
     ▼
SQL Validation & Sanitization
     │
     ▼
MySQL Database
     │
     ▼
Results Displayed in Streamlit
```

---

# 🛠️ Technology Stack

| Component          | Technology             |
| ------------------ | ---------------------- |
| Frontend           | Streamlit              |
| Backend            | Python                 |
| AI Model           | Gemini API             |
| Database           | MySQL                  |
| Database Connector | mysql-connector-python |
| Data Processing    | Pandas                 |
| Deployment         | Streamlit Cloud        |

---

# ✨ Features

* Convert natural language into SQL queries
* Execute SQL queries on a MySQL database
* Interactive Streamlit dashboard
* Download query results as CSV
* Session state management using Streamlit
* SQL output sanitization before execution
* Secure API key management using Streamlit Secrets

---

# 📂 Project Structure

```text
SQL-Query-Generator/
│
├── ui.py
├── requirements.txt
├── README.md
├── app.py
├── database.py
└── .streamlit/
    └── secrets.toml
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/premchavan-308/AI-Powered-SQL-Navigator.git

cd SQL-Query-Generator
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🗄️ Database Setup

Create a sample database:

```sql
CREATE DATABASE test_db;

USE test_db;

CREATE TABLE employees (
    id INT PRIMARY KEY,
    name VARCHAR(50)
);

INSERT INTO employees VALUES
(1,'Alice'),
(2,'Bob'),
(3,'Charlie');
```

---

# 🔐 Environment Configuration

Create `.streamlit/secrets.toml`

```toml
GEMINI_API_KEY = "YOUR_API_KEY"

MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_DATABASE = "test_db"
MYSQL_USER = "root"
MYSQL_PASSWORD = "password"
```

# 🌐 Deployment

The application can be deployed on Streamlit Cloud.

For cloud deployment:

1. Push code to GitHub
2. Deploy repository on Streamlit Cloud
3. Add database credentials and Gemini API key to Streamlit Secrets
4. Configure remote database access

---

# 🔍 Challenges Faced

### 1. Gemini Output Formatting

Gemini often returned SQL inside Markdown blocks:

```sql
SELECT * FROM employees;
```

This caused execution issues.

**Solution:** Added output sanitization to remove markdown wrappers before execution.

### 2. Session State Management

Generated SQL disappeared during page reruns.

**Solution:** Used `st.session_state` to persist generated queries and results.

### 3. Database Connectivity

Cloud deployments cannot directly access local databases.

**Solution:** Configured remote database access and tested secure connectivity between Streamlit Cloud and MySQL.

---

# 📈 Future Enhancements

* Query history tracking
* Database schema visualization
* Support for PostgreSQL and MongoDB
* User authentication
* Query explanation and optimization suggestions
* Role-based database access

---

# 👨‍💻 Author

Prem Ramdas Chavan

Bachelor of Engineering (BE)

AI-Powered Database Querying using Large Language Models and Generative AI


---
