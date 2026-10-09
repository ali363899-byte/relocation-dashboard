import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DB_PATH = "relocation.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                country TEXT NOT NULL,
                university TEXT NOT NULL,
                visa_status TEXT DEFAULT 'Pending Review',
                housing_status TEXT DEFAULT 'Unassigned',
                documents_cleared INTEGER DEFAULT 0
            )
        ''')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM students")
        if cursor.fetchone()[0] == 0:
            sample_records = [
                ("Ahmed Mansoor", "Tunisia", "Ajman University", "Approved", "Assigned", 1),
                ("Youssef Ben Ali", "Tunisia", "JUST Irbid", "Processing", "In Progress", 0),
                ("Sarah Khemir", "Tunisia", "University of Jordan", "Approved", "Assigned", 1)
            ]
            conn.executemany('''
                INSERT INTO students (full_name, country, university, visa_status, housing_status, documents_cleared)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', sample_records)
            conn.commit()

init_db()

@app.route("/")
def index():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
    return render_template("index.html", students=students)

@app.route("/add", methods=["POST"])
def add_student():
    name = request.form["full_name"]
    country = request.form["country"]
    university = request.form["university"]
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            INSERT INTO students (full_name, country, university, visa_status, housing_status, documents_cleared)
            VALUES (?, ?, ?, 'Pending Review', 'Unassigned', 0)
        ''', (name, country, university))
        conn.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
