from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="course_user",
        password="Course@123",
        database="course_registration"
    )

def fetch_all(query):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data

def fetch_one(query):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query)
    data = cursor.fetchone()
    cursor.close()
    db.close()
    return data

@app.route("/")
def home():
    stats = {
        "students": fetch_one("SELECT COUNT(*) AS total FROM students")["total"],
        "professors": fetch_one("SELECT COUNT(*) AS total FROM professors")["total"],
        "courses": fetch_one("SELECT COUNT(*) AS total FROM courses")["total"],
        "registrations": fetch_one("SELECT COUNT(*) AS total FROM registrations")["total"]
    }

    featured_professor = fetch_one("""
        SELECT * FROM professors
        WHERE full_name = 'Aaron Crandall'
        LIMIT 1
    """)

    popular_courses = fetch_all("""
        SELECT 
            c.course_name,
            p.full_name AS professor_name,
            COUNT(r.registration_id) AS enrollments
        FROM courses c
        LEFT JOIN professors p ON c.professor_id = p.professor_id
        LEFT JOIN registrations r ON c.course_id = r.course_id
        GROUP BY c.course_id, c.course_name, p.full_name
        ORDER BY
            CASE WHEN c.course_name = 'Cloud Computing' THEN 0 ELSE 1 END,
            enrollments DESC
        LIMIT 5
    """)

    return render_template(
        "index.html",
        stats=stats,
        featured_professor=featured_professor,
        popular_courses=popular_courses
    )

@app.route("/students")
def students():
    students = fetch_all("SELECT * FROM students ORDER BY student_id")
    return render_template("students.html", students=students)

@app.route("/professors")
def professors():
    professors = fetch_all("""
        SELECT 
            p.professor_id,
            p.full_name,
            p.subject,
            p.specialization,
            p.experience,
            COUNT(c.course_id) AS courses_count
        FROM professors p
        LEFT JOIN courses c ON p.professor_id = c.professor_id
        GROUP BY p.professor_id, p.full_name, p.subject, p.specialization, p.experience
        ORDER BY p.professor_id
    """)
    return render_template("professors.html", professors=professors)

@app.route("/courses")
def courses():
    courses = fetch_all("""
        SELECT
            c.course_id,
            c.course_name,
            p.full_name AS professor_name,
            c.credits,
            c.capacity,
            COUNT(r.registration_id) AS enrollments
        FROM courses c
        LEFT JOIN professors p ON c.professor_id = p.professor_id
        LEFT JOIN registrations r ON c.course_id = r.course_id
        GROUP BY c.course_id, c.course_name, p.full_name, c.credits, c.capacity
        ORDER BY
            CASE WHEN c.course_name = 'Cloud Computing' THEN 0 ELSE 1 END,
            enrollments DESC,
            c.course_name ASC
    """)
    return render_template("courses.html", courses=courses)

@app.route("/registrations")
def registrations():
    registrations = fetch_all("""
        SELECT
            r.registration_id,
            s.full_name AS student_name,
            s.department,
            c.course_name,
            p.full_name AS professor_name,
            r.registration_date,
            r.status
        FROM registrations r
        JOIN students s ON r.student_id = s.student_id
        JOIN courses c ON r.course_id = c.course_id
        LEFT JOIN professors p ON c.professor_id = p.professor_id
        ORDER BY r.registration_id
    """)
    return render_template("registrations.html", registrations=registrations)

@app.route("/student/<int:student_id>")
def student_profile(student_id):
    student = fetch_one(f"""
        SELECT * FROM students
        WHERE student_id = {student_id}
    """)

    courses = fetch_all(f"""
        SELECT
            c.course_name,
            c.credits,
            p.full_name AS professor_name,
            r.registration_date,
            r.status
        FROM registrations r
        JOIN courses c ON r.course_id = c.course_id
        LEFT JOIN professors p ON c.professor_id = p.professor_id
        WHERE r.student_id = {student_id}
        ORDER BY c.course_name
    """)

    total_credits = sum(course["credits"] for course in courses)

    return render_template(
        "student_profile.html",
        student=student,
        courses=courses,
        total_credits=total_credits
    )
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
