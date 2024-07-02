**Test Case Management System**


This is a web application built using Flask and MySQL to manage and compare test cases. The system allows users to register, log in, add test cases, create versions, edit test cases, and more.



**Features:**


User registration and authentication,

Adding, editing, and deleting test cases,

Creating and deleting versions,

Viewing all test cases,

Secure session management


**Prerequisites**


Python 3.x,

MySQL



**Installation**

Clone the repository:

git clone https://github.com/yourusername/test-case-management.git

cd test-case-management



Create a virtual environment:

python -m venv venv,

source venv/bin/activate   # On Windows, use `venv\Scripts\activate`


Install the required packages:

Flask,

mysql.connector


**Set up the MySQL database:**

Create a MySQL database named aditya2,

Update the MySQL configuration in app.py with your MySQL username and password.


Run the database setup:

python app.py


**Configuration**
In the app.py file, update the following MySQL configurations as per your setup:

python:
MYSQL_USER = 'your_mysql_user'
MYSQL_PASSWORD = 'your_mysql_password'
MYSQL_HOST = 'localhost'
MYSQL_DATABASE = 'aditya2'
Running the Application


Start the Flask application:

python app.py


Open your web browser and navigate to:

http://127.0.0.1:5000/


**Usage**

Register a new user,

Log in using the registered credentials,

Add test cases and create versions,

Edit or delete test cases,

View all test cases and their versions.


**File Structure:**

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


**Troubleshooting**

Database Connection Errors:

Ensure your MySQL service is running and the credentials in app.py are correct.

Page Not Loading:

Check the Flask application logs for any errors.

License

This project is licensed under the MIT License. See the LICENSE file for details.
