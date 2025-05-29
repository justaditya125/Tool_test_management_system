# 🚀 Test Case Management System

A **web-based application** built using **Flask** and **MySQL** to manage and compare test cases with support for multiple versions.

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Flask](https://img.shields.io/badge/Flask-%23000.svg?style=flat&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-005C84?style=flat&logo=mysql&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## ✨ Features

- ✅ User registration and login  
- ➕ Add/Edit/Delete test cases  
- 🧬 Create and manage versions  
- 🔒 Secure session management  
- 📄 View all test cases and their versions  

---

## 📦 Requirements

To run this project locally, you will need:

- **Python 3.x**  
- **MySQL Server**  
- **pip (Python package manager)**  

---

## 🔧 Installation Guide

Follow these steps to set up the project on your local machine:

### 📁 Step 1: Clone the Repository

```bash
git clone https://github.com/justaditya125/test-case-management.git
cd test-case-management
🐍 Step 2: Set Up a Virtual Environment (Recommended)
On macOS/Linux:
bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate
On Windows:
bash
Copy
Edit
python -m venv venv
venv\Scripts\activate
📦 Step 3: Install Python Dependencies
If a requirements.txt file is provided:

bash
Copy
Edit
pip install -r requirements.txt
Or install manually:

bash
Copy
Edit
pip install flask mysql-connector-python
🛠️ Step 4: Set Up the MySQL Database
✅ 1. Open MySQL Command Line:
bash
Copy
Edit
mysql -u root -p
Enter your MySQL root password when prompted.

✅ 2. Create the Database:
sql
Copy
Edit
CREATE DATABASE database;
⚙️ Step 5: Configure app.py
Open app.py and update these variables with your MySQL credentials:

python
Copy
Edit
MYSQL_USER = 'your_mysql_user'
MYSQL_PASSWORD = 'your_mysql_password'
MYSQL_HOST = 'localhost'
MYSQL_DATABASE = 'database'
▶️ Step 6: Run the Application
Start the Flask app:

bash
Copy
Edit
python app.py
Flask will start a development server. Open your browser and visit:

cpp
Copy
Edit
http://127.0.0.1:5000/
🧪 How to Use
✅ Register a new user

🔐 Log in with your credentials

➕ Add test cases

📝 Edit or delete test cases

🧬 Create and manage versions

📄 View all test cases and versions

📁 Project Structure
arduino
Copy
Edit
test-case-management/
│
├── templates/
│   ├── home.html
│   ├── register.html
│   ├── login.html
│   ├── index2.html
│   ├── add_test_case1.html
│   ├── edit_test_case1.html
│   ├── create_version.html
│   ├── add_other_test_case.html
│   └── all_test_cases.html
│
├── app.py
├── requirements.txt
└── README.md
🧰 Troubleshooting
❌ MySQL Connection Error
Make sure MySQL is running

Double-check your username/password in app.py

Ensure the database exists

⚠️ Flask Page Not Loading
Check the terminal output for Flask errors

Make sure you're visiting http://127.0.0.1:5000/

Verify HTML files are inside the templates/ folder

📄 License
This project is licensed under the MIT License.
See the LICENSE file for more information.

🤝 Contributing
Fork the repository

Create a new branch:

bash
Copy
Edit
git checkout -b feature-name
Make your changes

Commit:

bash
Copy
Edit
git commit -m "Added new feature"
Push:

bash
Copy
Edit
git push origin feature-name
Open a Pull Request

📬 Contact
ADITYA SAH
📧 aditya57671@gmail.com
🌐 GitHub - justaditya125

📚 This README Includes:
✅ Full setup commands (even for absolute beginners)

✅ Clear MySQL instructions

✅ Virtual environment guidance

✅ Examples for each configuration step

✅ Project overview and features

Let me know if you want to add screenshots, ER diagrams, Docker setup, or deployment instructions to make it even more complete!

yaml
Copy
Edit

---

You can copy this entire block at once and paste it into your README.md file.  

If you want, I can also help you create a ready-to-download `.md` file with this content. Just say the wo
