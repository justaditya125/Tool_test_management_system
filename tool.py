from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, send_file
import mysql.connector
import datetime
import csv
import io

app = Flask(__name__)
app.secret_key = 'secret_key'
DATABASE = 'aditya2'

# MySQL Configuration
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456789'
MYSQL_HOST = 'localhost'
MYSQL_DATABASE = 'aditya2'

def connect_db():           
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123456789',
            database=DATABASE
        )
        return conn
    except mysql.connector.Error as e:
        print("Error connecting to database:", e)
        return None

def create_tables():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            # Create users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username VARCHAR(255) PRIMARY KEY,
                    email VARCHAR(255),
                    password VARCHAR(255)
                )
            ''')

            # Create versions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS versions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    version_number INT
                )
            ''')

            # Create test_cases table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS test_cases (
                    id VARCHAR(255) PRIMARY KEY
                )
            ''')

            # Create version_tables table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS version_tables (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    version_id INT,
                    test_case_id VARCHAR(255),
                    description TEXT,
                    result TEXT,
                    remarks TEXT,
                    FOREIGN KEY (test_case_id) REFERENCES test_cases(id),
                    FOREIGN KEY (version_id) REFERENCES versions(id)
                )
            ''')

            # Create result_id table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS result_id (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    version_id INT,
                    test_case_id VARCHAR(255),
                    description TEXT,
                    result TEXT,
                    remarks TEXT,
                    FOREIGN KEY (version_id) REFERENCES versions(id),
                    FOREIGN KEY (test_case_id) REFERENCES test_cases(id)
                )
            ''')

            conn.commit()
        except mysql.connector.Error as e:
            print(f"Error creating tables: {e}")
        finally:
            cursor.close()
            conn.close()

create_tables()

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123456789',
            database=DATABASE
        )
        return conn
    except mysql.connector.Error as e:
        print("Error connecting to database:", e)
        return None

def get_ids():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM test_cases")
            ids = [row[0] for row in cursor.fetchall()]
            return ids
        except mysql.connector.Error as e:
            print(f"Error fetching IDs: {e}")
        finally:
            cursor.close()
            conn.close()
    return []

def get_versions():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id, version_number FROM versions ORDER BY version_number DESC")
            versions = cursor.fetchall()
            return versions
        except mysql.connector.Error as e:
            print("Error fetching versions:", e)
        finally:
            cursor.close()
            conn.close()
    return []

def get_test_cases():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT tc.id, tc.description, tc.result, tc.remarks, v.version_number
                FROM test_cases tc
                LEFT JOIN version_tables vt ON tc.id = vt.test_case_id
                LEFT JOIN versions v ON vt.version_id = v.id
            """)
            test_cases = cursor.fetchall()
            return jsonify({'test_cases': test_cases})
        except mysql.connector.Error as e:
            print("Error fetching test cases:", e)
        finally:
            cursor.close()
            conn.close()
    return jsonify({'test_cases': []})

def generate_split_id(data):
    today_date = datetime.datetime.today().date().strftime("%d%m%y")
    return f"{data}"

# User authentication functions
def user_exists(username, email):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=%s OR email=%s", (username, email))
    user = cur.fetchone()
    conn.close()
    return user

def verify_user(username, password):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cur.fetchone()
    conn.close()
    return user


#index
@app.route('/')
def home():
    return render_template('home.html')


#register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if user_exists(username, email):
            flash('Username or email already exists!', 'error')
        else:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s)', (username, email, password))
            conn.commit()
            conn.close()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')


#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if verify_user(username, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')


#logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


#index2
@app.route('/index')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index2.html')


#add test case
@app.route('/add_test_case', methods=['GET', 'POST'])
def add_test_case():
    versions = get_versions()

    if request.method == 'POST':
        try:
            id = request.form['data'].strip()

            if not id :
                flash("Error: 'ID' fields are required.", "error")
                return redirect(url_for('add_test_case'))

            conn = get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()

                    # Insert into test_cases table if not exists
                    sql_insert_test_case = "INSERT IGNORE INTO test_cases (id) VALUES (%s)"
                    cursor.execute(sql_insert_test_case, (id,))

                    conn.commit()
                    flash("Test case added successfully", "success")
                    return redirect(url_for('all_test_cases'))
                
                except mysql.connector.Error as e:
                    print(f"Error inserting data: {e}")
                    conn.rollback()
                    flash(f"Error inserting data: {e}. Please try again.", "error")
                
                finally:
                    cursor.close()
                    conn.close()
            
            else:
                flash("Database connection failed. Please try again later.", "error")

        except KeyError as e:
            flash(f"KeyError: {str(e)}", "error")
            return redirect(url_for('add_test_case'))

    return render_template('add_test_case1.html', versions=versions)



#edit test case
@app.route('/edit_test_case/<string:test_case_id>', methods=['GET', 'POST'])
def edit_test_case(test_case_id):
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed. Please try again later.", "error")
        return redirect(url_for('all_test_cases'))
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Fetch the existing test case data
        cursor.execute("""
            SELECT tc.id, ri.description, ri.result, ri.remarks, v.version_number, v.id as version_id
            FROM test_cases tc
            LEFT JOIN result_id ri ON tc.id = ri.test_case_id
            LEFT JOIN versions v ON ri.version_id = v.id
            WHERE tc.id = %s
        """, (test_case_id,))
        test_case = cursor.fetchone()
     
        if not test_case:
            flash("Test case not found.", "error")
            return redirect(url_for('all_test_cases'))
        
        if request.method == 'POST':
            description = request.form.get('description', '')
            result = request.form.get('result', '')
            remarks = request.form.get('remarks', '')
            version_id = request.form.get('version_id')
            
            if not version_id:
                flash("Version ID is required.", "error")
                return redirect(url_for('edit_test_case', test_case_id=test_case_id))
            
            # Check if there's an existing record in result_id
            cursor.execute("SELECT * FROM result_id WHERE test_case_id = %s AND version_id = %s", (test_case_id, version_id))
            existing_result = cursor.fetchone()
            
            if existing_result:
                # Update existing record
                update_query = """
                    UPDATE result_id 
                    SET description = %s, result = %s, remarks = %s
                    WHERE test_case_id = %s AND version_id = %s
                """
                cursor.execute(update_query, (description, result, remarks, test_case_id, version_id))
            else:
                # Insert new record
                insert_query = """
                    INSERT INTO result_id (test_case_id, version_id, description, result, remarks) 
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (test_case_id, version_id, description, result, remarks))
            
            conn.commit()
            
            if cursor.rowcount > 0:
                flash("Test case updated successfully", "success")
            else:
                flash("No changes were made to the test case", "info")
            
            return redirect(url_for('all_test_cases'))
        
        # Fetch all versions for the dropdown
        cursor.execute("SELECT id, version_number FROM versions")
        versions = cursor.fetchall()
        
        return render_template('edit_test_case1.html', test_case=test_case, versions=versions)
    
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
        flash(f"Error updating test case: {e}. Please try again.", "error")
    
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('all_test_cases'))



#delete test case
@app.route('/delete_test_case/<string:test_case_id>/<int:version_id>', methods=['POST'])
def delete_test_case(test_case_id, version_id):
    conn = get_db_connection()
    
    if not conn:
        flash("Database connection failed. Please try again later.", "error")
        return redirect(url_for('all_test_cases'))
    
    try:
        cursor = conn.cursor()
        
        # Delete only from result_id table for the specific version
        cursor.execute("DELETE FROM result_id WHERE test_case_id = %s AND version_id = %s", (test_case_id, version_id))
        
        # We're not deleting from test_cases table as the test case itself should remain
        # We're also not deleting from version_tables as it might contain data for other versions
        
        conn.commit()
        flash(f"Deleted data for test case ID {test_case_id} in version {version_id}", "success")
    
    except mysql.connector.Error as e:
        print(f"Error deleting test case data: {e}")
        conn.rollback()
        flash("Error deleting test case data. Please try again.", "error")
    
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('all_test_cases'))



# create version
@app.route('/create_version', methods=['GET', 'POST'])
def create_version():
    if request.method == 'POST':
        try:
            version_number = int(request.form['version_number'])
            conn = get_db_connection()
            
            if conn:
                cursor = conn.cursor()
                
                try:
                    sql_insert_version = "INSERT INTO versions (version_number) VALUES (%s)"
                    cursor.execute(sql_insert_version, (version_number,))
                    conn.commit()
                    flash(f"Version '{version_number}' created successfully", "success")
                
                except mysql.connector.Error as e:
                    print(f"Error inserting version: {e}")
                    conn.rollback()
                    flash(f"Error inserting version '{version_number}': {e}", "error")
                
                finally:
                    cursor.close()
                    conn.close()
            
            else:
                flash("Database connection failed. Please try again later.", "error")
        
        except ValueError:
            flash("Invalid version number. Please enter a valid integer.", "error")
    
    versions = get_versions()
    
    return render_template('create_version.html', versions=versions)



#delete version
@app.route('/delete_version/<int:version_id>', methods=['POST'])
def delete_version(version_id):
    conn = get_db_connection()
    
    if not conn:
        flash("Database connection failed. Please try again later.", "error")
        return redirect(url_for('create_version'))
    
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM result_id WHERE version_id = %s", (version_id,))
        cursor.execute("DELETE FROM version_tables WHERE version_id = %s", (version_id,))
        cursor.execute("DELETE FROM versions WHERE id = %s", (version_id,))
        conn.commit()
        flash(f"Deleted version with id {version_id}", "success")
    
    except mysql.connector.Error as e:
        print(f"Error deleting version: {e}")
        conn.rollback()
        flash("Error deleting version. Please try again.", "error")
    
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('create_version'))



#create result test case
@app.route('/add_other_test_case', methods=['GET', 'POST'])
def add_other_test_case():
    versions = get_versions()
    ids = get_ids()

    if request.method == 'POST':
        try:
            id = request.form['id'].strip()
            description = request.form['description']
            result = request.form['result']
            remarks = request.form['remarks']
            version_id = request.form['version_id']

            if not id or not version_id:
                flash("Error: 'ID' and 'Version' fields are required.", "error")
                return redirect(url_for('add_other_test_case'))

            conn = get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    # Then, insert or update the result in the result_id table
                    sql_insert_result_id = """
                    INSERT INTO result_id (version_id, test_case_id, description, result, remarks) 
                    VALUES (%s, %s, %s, %s, %s) 
                    ON DUPLICATE KEY UPDATE result = %s, remarks = %s
                    """
                    cursor.execute(sql_insert_result_id, (version_id, id, description, result, remarks, result, remarks))

                    conn.commit()
                    flash("Other test case added successfully", "success")
                    return redirect(url_for('all_test_cases'))

                except mysql.connector.Error as e:
                    print(f"Error inserting data: {e}")
                    conn.rollback()
                    flash(f"Error inserting data: {e}. Please try again.", "error")
                finally:
                    cursor.close()
                    conn.close()
            else:
                flash("Database connection failed. Please try again later.", "error")

        except KeyError as e:
            flash(f"KeyError: {str(e)}", "error")
            return redirect(url_for('add_other_test_case'))

    return render_template('add_other_test_case.html', versions=versions, ids=ids)



#all test case
@app.route('/all_test_cases')
def all_test_cases():
    conn = get_db_connection()
    
    if not conn:
        flash("Database connection failed. Please try again later.", "error")
        return redirect(url_for('index'))
    
    cursor = conn.cursor(dictionary=True)
    
    try:
     cursor.execute("""
    SELECT tc.id, ri.description, ri.result, ri.remarks, v.version_number, v.id as version_id
    FROM result_id ri
    JOIN test_cases tc ON ri.test_case_id=tc.id
    JOIN versions v ON ri.version_id = v.id
""")
     test_cases = cursor.fetchall()
    
    except mysql.connector.Error as e:
        print(f"Error fetching data: {e}")
        flash("Error fetching data. Please try again.", "error")
        test_cases = []
    
    finally:
        cursor.close()
        conn.close()
    
    return render_template('all_test_cases.html', test_cases=test_cases)


#view version data
@app.route('/view_version_data/<int:version_id>')
def view_version_data(version_id):
    conn = get_db_connection()

    if not conn:
        flash("Database connection failed. Please try again later.", "error")
        return redirect(url_for('index'))  # Redirect to an appropriate page if database connection fails

    try:
        cursor = conn.cursor(dictionary=True)

        # Fetch version details
        cursor.execute("SELECT id, version_number FROM versions WHERE id = %s", (version_id,))
        version_data = cursor.fetchone()

        if not version_data:
            flash("Version not found.", "error")
            return redirect(url_for('create_version'))  # Redirect to an appropriate page if version not found

        # Fetch test cases for the specified version
        cursor.execute("""
    SELECT tc.id, ri.description, ri.result, ri.remarks
    FROM test_cases tc
    LEFT JOIN result_id ri ON tc.id = ri.test_case_id
    WHERE ri.version_id = %s
""", (version_id,))


        test_case_data = cursor.fetchall()

        if not test_case_data:
            flash("No test cases found for this version.", "info")  # Adjusted message to inform about no test cases
            return render_template('view_version_data.html', version_data=version_data, test_case_data=test_case_data)

        return render_template('view_version_data.html', version_data=version_data, test_case_data=test_case_data)

    except mysql.connector.Error as e:
        print(f"Error fetching version and test case data: {e}")
        flash(f"Error fetching data: {e}. Please try again later.", "error")
        return redirect(url_for('index'))  # Redirect to an appropriate page on error

    finally:
        cursor.close()
        conn.close()



# compare data
@app.route('/compare_data')
def compare_data():
    conn = get_db_connection()

    if not conn:
        flash("Database connection failed. Please try again later.", "error")
        return redirect(url_for('all_test_cases'))

    cursor = conn.cursor(dictionary=True)

    try:
        # Fetch all test case IDs
        cursor.execute("SELECT id FROM test_cases ORDER BY id")
        test_case_ids = [row['id'] for row in cursor.fetchall()]

        # Fetch all versions
        cursor.execute("SELECT id, version_number FROM versions ORDER BY version_number")
        versions = cursor.fetchall()

        # Create a dictionary to store results in a format suitable for rendering
        comparison_data = {}

        # Iterate through each version and fetch results for each test case ID
        for version in versions:
            version_id = version['id']
            version_number = version['version_number']

            # Fetch results for the current version and concatenate them into a list
            cursor.execute("""
                SELECT tc.id, ri.result
                FROM test_cases tc
                LEFT JOIN result_id ri ON tc.id = ri.test_case_id AND ri.version_id = %s
                ORDER BY tc.id
            """, (version_id,))
            results = cursor.fetchall()

            # Store results in the dictionary, using test case ID as the key
            for result in results:
                test_case_id = result['id']
                result_value = result['result']

                if test_case_id not in comparison_data:
                    comparison_data[test_case_id] = {}

                comparison_data[test_case_id][version_number] = result_value if result_value is not None else ''

    except mysql.connector.Error as e:
        print(f"Error fetching data: {e}")
        comparison_data = {}
        flash("Error fetching data. Please try again.", "error")

    finally:
        cursor.close()
        conn.close()

    return render_template('compare_data.html', comparison_data=comparison_data, test_case_ids=test_case_ids, versions=versions)



#export csv
@app.route('/export_csv', methods=['GET'])
def export_csv():     
    conn = get_db_connection()

    if not conn:
        flash("Database connection failed. Please try again later.", "error")
        return redirect(url_for('index'))

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT tc.id, ri.description, ri.result, ri.remarks, v.version_number
            FROM test_cases tc
            LEFT JOIN result_id ri ON tc.id = ri.test_case_id
            LEFT JOIN versions v ON ri.version_id = v.id
            ORDER BY tc.id, v.version_number
        """)
        test_cases = cursor.fetchall()

        # Create a CSV output in-memory
        output = io.StringIO()
        writer = csv.writer(output)

        # Write header row
        writer.writerow(['ID', 'Description', 'Result', 'Remarks', 'Version'])

        # Write rows
        for test_case in test_cases:
            writer.writerow([
                test_case['id'],
                test_case['description'] or '',
                test_case['result'] or '',
                test_case['remarks'] or '',
                test_case['version_number'] or ''
            ])

        output.seek(0)

        # Generate a default filename
        default_filename = 'test_cases.csv'

        # Send the CSV file as an attachment, allowing the browser to prompt for save location
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=default_filename
        )
    # exceptional handling
    except mysql.connector.Error as e:
        print(f"Error fetching data: {e}")
        flash("Error fetching data. Please try again.", "error")
        return redirect(url_for('index'))

    finally:
        cursor.close()
        conn.close()

# close flask
if __name__ == '__main__':
    app.run(debug=True)