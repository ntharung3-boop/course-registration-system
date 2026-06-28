from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)
db = mysql.connector.connect(
    host="localhost",
    user="course_user",
    password="Course@123",
    database="course_registration"
)

cursor = db.cursor(dictionary=True)
@app.route("/")
def home():
    cursor.execute("SELECT COUNT(*) AS total FROM students")
    total_students = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM courses")
    total_courses = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM registrations")
    total_registrations = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM professors")
    total_professors = cursor.fetchone()["total"]

    return render_template(
        "index.html",
        total_students=total_students,
        total_courses=total_courses,
        total_registrations=total_registrations,
       total_professors=total_professors
    )
@app.route("/students")
def students():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    return render_template("students.html", students=students)

@app.route("/courses")
def courses():
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    return render_template("courses.html", courses=courses)

@app.route("/register-course", methods=["GET", "POST"])
def register_course():
    if request.method == "POST":
        student_id = request.form["student_id"]
        course_id = request.form["course_id"]

        cursor.execute(
            "INSERT INTO registrations (student_id, course_id) VALUES (%s, %s)",
            (student_id, course_id)
        )
        db.commit()

        return redirect(url_for("registrations"))

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()

    return render_template(
        "register_course.html",
        students=students,
        courses=courses
    )

@app.route("/registrations")
def registrations():
    query = """
SELECT
    registrations.registration_id,
    students.full_name AS student_name,
    students.department,
    courses.course_name,
    professors.full_name AS professor_name,
    registrations.status,
    registrations.registration_date
FROM registrations
JOIN students
    ON registrations.student_id = students.student_id
JOIN courses
    ON registrations.course_id = courses.course_id
LEFT JOIN professors
    ON courses.professor_id = professors.professor_id
ORDER BY registrations.registration_id DESC
"""
    cursor.execute(query)
    registrations = cursor.fetchall()
    return render_template("registrations.html", registrations=registrations)
@app.route("/add-student", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        full_name = request.form["full_name"]
        email = request.form["email"]
        department = request.form["department"]
        semester = request.form["semester"]

        cursor.execute(
            """
            INSERT INTO students (full_name, email, department, semester)
            VALUES (%s, %s, %s, %s)
            """,
            (full_name, email, department, semester)
        )
        db.commit()

        return redirect(url_for("students"))

    return render_template("add_student.html")
@app.route("/add-course", methods=["GET", "POST"])
def add_course():

    cursor.execute("SELECT professor_id, full_name FROM professors")
    professors = cursor.fetchall()

    if request.method == "POST":

        course_name = request.form["course_name"]
        professor_id = request.form["professor_id"]
        credits = request.form["credits"]
        capacity = request.form["capacity"]

        cursor.execute("""
            INSERT INTO courses
            (course_name, professor_id, credits, capacity)
            VALUES (%s,%s,%s,%s)
        """,
        (course_name, professor_id, credits, capacity))

        db.commit()

        return redirect(url_for("courses"))

    return render_template(
        "add_course.html",
        professors=professors
    )
@app.route("/delete-registration/<int:registration_id>")
def delete_registration(registration_id):
    cursor.execute(
        "DELETE FROM registrations WHERE registration_id = %s",
        (registration_id,)
    )
    db.commit()

    return redirect(url_for("registrations"))
@app.route("/delete-course/<int:course_id>")
def delete_course(course_id):
    try:
        cursor.execute(
            "DELETE FROM courses WHERE course_id = %s",
            (course_id,)
        )
        db.commit()
    except Exception as e:
        db.rollback()
        print("Error deleting course:", e)

    return redirect(url_for("courses"))

@app.route("/professors")
def professors():
    cursor.execute("SELECT * FROM professors")
    professors = cursor.fetchall()
    return render_template("professors.html", professors=professors)
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
