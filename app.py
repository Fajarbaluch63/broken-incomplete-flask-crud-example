from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MySQL configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'secret'
app.config['MYSQL_DB'] = 'student'
app.config['MYSQL_HOST'] = '34.147.154.231'

mysql = MySQL(app)

# Function to execute queries safely
def execute_query(query, params=None):
    try:
        cur = mysql.connection.cursor()
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        mysql.connection.commit()
        return True
    except Exception as e:
        app.logger.error(f"Error executing query: {e}")
        return False

# Routes
@app.route("/add", methods=['POST'])
def add_student():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    query = "INSERT INTO students(studentName, email) VALUES(%s, %s);"
    success = execute_query(query, (name, email))
    if success:
        return jsonify(Result="Success")
    else:
        return jsonify(Result="Error"), 500

@app.route("/update", methods=['PUT'])
def update_student():
    data = request.get_json()
    student_id = data.get('id')
    name = data.get('name')
    email = data.get('email')
    query = "UPDATE students SET studentName = %s, email = %s WHERE studentID = %s;"
    success = execute_query(query, (name, email, student_id))
    if success:
        return jsonify(Result="Success")
    else:
        return jsonify(Result="Error"), 500

@app.route("/delete", methods=['DELETE'])
def delete_student():
    name = request.get_json().get('name')
    query = "DELETE FROM students WHERE studentName=%s;"
    success = execute_query(query, (name,))
    if success:
        return jsonify(Result="Success")
    else:
        return jsonify(Result="Error"), 500

@app.route("/default")
def list_students():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM students")
        rows = cur.fetchall()
        students = [{"ID": row[2], "Name": row[0], "Email": row[1]} for row in rows]
        return jsonify(Results=students, count=len(students))
    except Exception as e:
        app.logger.error(f"Error retrieving students: {e}")
        return jsonify(Result="Error", Message="Could not retrieve students."), 500

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
