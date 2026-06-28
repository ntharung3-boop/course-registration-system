DROP TABLE IF EXISTS registrations;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS professors;
DROP TABLE IF EXISTS students;

CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    department VARCHAR(100),
    semester INT
);

CREATE TABLE professors (
    professor_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    subject VARCHAR(100),
    specialization VARCHAR(200),
    experience VARCHAR(100)
);

CREATE TABLE courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(120) NOT NULL,
    professor_id INT,
    credits INT,
    capacity INT,
    FOREIGN KEY (professor_id) REFERENCES professors(professor_id)
);

CREATE TABLE registrations (
    registration_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    course_id INT,
    registration_date DATE,
    status VARCHAR(50),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

INSERT INTO professors (full_name, subject, specialization, experience) VALUES
('Aaron Crandall', 'Cloud Computing', 'Cloud Systems, Software Engineering, AI Applications', 'Professor / Cloud Computing Instructor'),
('Sarah Lewis', 'Artificial Intelligence', 'Machine Learning and Intelligent Systems', '10+ years'),
('Jennifer Clark', 'Data Engineering', 'Data Pipelines and Cloud Databases', '9+ years'),
('David Thompson', 'Web Application Development', 'Full Stack Web Systems', '8+ years'),
('Robert Wilson', 'Database Systems', 'SQL, Relational Databases, Data Modeling', '12+ years'),
('Emily Carter', 'Cyber Security', 'Network Security and Risk Management', '7+ years'),
('Michael Adams', 'Software Engineering', 'Agile Development and Architecture', '11+ years'),
('Laura Evans', 'Data Analytics', 'Business Intelligence and Visualization', '8+ years');

INSERT INTO courses (course_name, professor_id, credits, capacity) VALUES
('Cloud Computing', 1, 5, 40),
('Artificial Intelligence', 2, 5, 45),
('Data Engineering', 3, 5, 40),
('Web Application Development', 4, 5, 35),
('Database Management Systems', 5, 5, 50),
('Cyber Security', 6, 4, 35),
('Software Engineering', 7, 5, 45),
('Data Analytics', 8, 4, 50),
('Machine Learning', 2, 5, 40),
('Data Visualization', 8, 4, 45),
('Computer Networks', 6, 4, 35),
('Big Data Analytics', 3, 5, 40);
