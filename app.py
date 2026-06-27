from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Nagula@2001",
    database="course_registration"
)

cursor = db.cursor(dictionary=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/students")
def students():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    return render_template("students.html", students=students)

@app.route("/courses")
def courses():

    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM courses")

    data = cursor.fetchall()

    cursor.close()

    return render_template(
        "courses.html",
        courses=data
    )

@app.route("/registrations")
def registrations():
    query = """
    SELECT
        registrations.registration_id,
        students.full_name,
        courses.course_name,
        registrations.registration_date
    FROM registrations
    JOIN students ON registrations.student_id = students.student_id
    JOIN courses ON registrations.course_id = courses.course_id
    """
    cursor.execute(query)
    registrations = cursor.fetchall()
    return render_template("registrations.html", registrations=registrations)

if __name__ == "__main__":
    app.run(debug=True)