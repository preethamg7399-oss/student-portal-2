from flask import Flask, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

if __name__ == "__main__":
    app.run()

# Used to protect the login session
app.secret_key = os.environ.get("SECRET_KEY", "local-testing-secret")


# Connect to database
def get_db():
connection = sqlite3.connect("/tmp/students.db")
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    connection = get_db()

    connection.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    connection.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        usn TEXT UNIQUE NOT NULL,
        address TEXT NOT NULL,
        email TEXT NOT NULL,
        college TEXT NOT NULL,
        phone TEXT NOT NULL,
        course TEXT NOT NULL,
        semester TEXT NOT NULL
    )
    """)

    connection.commit()
    connection.close()

init_db()

# ---------------- LOGIN ----------------

@app.route("/", methods=["GET", "POST"])
def login():

    error = ""

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        connection = get_db()

        user = connection.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        connection.close()

        if user and check_password_hash(user["password"], password):

            session["user_id"] = user["id"]
            session["username"] = user["username"]

            return redirect("/information")

        error = "Invalid username or password!"

    return f"""
    <!DOCTYPE html>
    <html>

    <head>
        <title>Login</title>

        <style>
            body {{
                font-family: Arial;
                background: linear-gradient(135deg, #141e30, #243b55);
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }}

            .box {{
                background: white;
                padding: 40px;
                width: 330px;
                border-radius: 15px;
            }}

            h1 {{
                text-align: center;
            }}

            input {{
                width: 100%;
                padding: 12px;
                margin: 10px 0;
                box-sizing: border-box;
                border-radius: 8px;
                border: 1px solid #ccc;
            }}

            button {{
                width: 100%;
                padding: 12px;
                background: #243b55;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
            }}

            .error {{
                color: red;
                text-align: center;
            }}
        </style>

    </head>

    <body>

        <div class="box">

            <h1>Login 🔐</h1>

            <form method="POST">

                <input
                    type="text"
                    name="username"
                    placeholder="Username"
                    required
                >

                <input
                    type="password"
                    name="password"
                    placeholder="Password"
                    required
                >

                <button type="submit">LOGIN</button>

            </form>

            <p class="error">{error}</p>

        </div>

    </body>

    </html>
    """


# ---------------- INFORMATION FORM ----------------

@app.route("/information", methods=["GET", "POST"])
def information():

    # User must be logged in
    if "user_id" not in session:
        return redirect("/")

    if request.method == "POST":

        name = request.form["name"]
        usn = request.form["usn"]
        address = request.form["address"]
        email = request.form["email"]
        college = request.form["college"]
        phone = request.form["phone"]
        course = request.form["course"]
        semester = request.form["semester"]

        connection = get_db()

        connection.execute("""
            INSERT INTO students
            (name, usn, address, email, college, phone, course, semester)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            usn,
            address,
            email,
            college,
            phone,
            course,
            semester
        ))

        connection.commit()
        connection.close()

        return """
        <h1>Information Saved Successfully! ✅</h1>
        <p>Your information has been saved to the database.</p>
        """

    return """
    <!DOCTYPE html>
    <html>

    <head>

        <title>Student Information</title>

        <style>

            body {
                font-family: Arial;
                background: #f2f2f2;
                padding: 40px;
            }

            .box {
                max-width: 600px;
                margin: auto;
                background: white;
                padding: 35px;
                border-radius: 15px;
            }

            h1 {
                text-align: center;
            }

            label {
                display: block;
                margin-top: 15px;
                font-weight: bold;
            }

            input, textarea, select {
                width: 100%;
                padding: 12px;
                margin-top: 7px;
                box-sizing: border-box;
                border: 1px solid #ccc;
                border-radius: 8px;
            }

            textarea {
                height: 80px;
            }

            button {
                width: 100%;
                padding: 13px;
                margin-top: 25px;
                background: #243b55;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 17px;
            }

        </style>

    </head>

    <body>

        <div class="box">

            <h1>Student Information 📝</h1>

            <form method="POST">

                <label>Full Name</label>
                <input type="text" name="name" required>

                <label>USN</label>
                <input type="text" name="usn" required>

                <label>Address</label>
                <textarea name="address" required></textarea>

                <label>Email</label>
                <input type="email" name="email" required>

                <label>College</label>
                <input type="text" name="college" required>

                <label>Phone Number</label>
                <input type="tel" name="phone" required>

                <label>Course</label>
                <input type="text" name="course" required>

                <label>Semester</label>

                <select name="semester" required>

                    <option value="">Select Semester</option>
                    <option>1st Semester</option>
                    <option>2nd Semester</option>
                    <option>3rd Semester</option>
                    <option>4th Semester</option>
                    <option>5th Semester</option>
                    <option>6th Semester</option>
                    <option>7th Semester</option>
                    <option>8th Semester</option>

                </select>

                <button type="submit">
                    SAVE INFORMATION
                </button>

            </form>

        </div>

    </body>

    </html>
    """


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
