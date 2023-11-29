from flask import Flask, request, render_template
from flask_mysqldb import MySQL
from flask_cors import CORS
import json

mysql = MySQL()
app = Flask(__name__)
CORS(app)

# MySQL Instance configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'secret'
app.config['MYSQL_DB'] = 'student'
app.config['MYSQL_HOST'] = '34.125.170.207'
mysql.init_app(app)

def execute_query(query):
    try:
        cur = mysql.connection.cursor()
        print("Executing query:", query)
        cur.execute(query)
        mysql.connection.commit()
        print("Query executed successfully")
        return True
    except Exception as e:
        print("Error:", e)
        return False

@app.route("/add", methods=['POST'])  # Add Student
def add():
    name = request.json.get('name')
    email = request.json.get('email')
    try:
        query = '''INSERT INTO students(studentName, email) VALUES('{}', '{}');'''.format(name, email)
        success = execute_query(query)

        if success:
            return '{"Result": "Success"}'
        else:
            return '{"Result": "Error"}'
    except Exception as e:
        return '{"Result": "Error", "Message": "' + str(e) + '"}'

@app.route("/update", methods=['PUT'])  # Update Student
def update():
    id = int(request.json.get('id'))
    name = request.json.get('name')
    email = request.json.get('email')
    try:


        query = '''UPDATE students SET studentName = '{}', email = '{}' WHERE studentID = {} ;'''.format(name, email, id)
        print("Received Update Request. ID:", id, "Name:", name, "Email:", email)
        success = execute_query(query)
        print(success)
        return '{"Result": "Success"}'
    except Exception as e:
        return '{"Result": "Error", "Message": "' + str(e) + '"}'

@app.route("/delete", methods=['DELETE'])  # Delete Student
def delete():
    name = request.json.get('name')
    try:
        query = '''DELETE FROM students WHERE studentName='{}';'''.format(name)
        success = execute_query(query)
        print(success)
        return '{"Result": "Success"}'

    except Exception as e:
        return '{"Result": "Error", "Message": "' + str(e) + '"}'


@app.route("/default")  # Default - Show Data
def read():
    try:
        cur = mysql.connection.cursor()
        cur.execute('''SELECT * FROM students''')
        rv = cur.fetchall()
        Results = []
        for row in rv:
            Result = {}
            Result['Name'] = row[0].replace('\n', ' ')
            Result['Email'] = row[1]
            Result['ID'] = row[2]
            Results.append(Result)
        response = {'Results': Results, 'count': len(Results)}
        ret = app.response_class(
            response=json.dumps(response),
            status=200,
            mimetype='application/json'
        )
        return ret
    except Exception as e:
        return '{"Result": "Error", "Message": "' + str(e) + '"}'
    
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')
