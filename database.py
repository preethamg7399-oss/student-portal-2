import sqlite3

connection = sqlite3.connect("students.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

cursor.execute("""
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

print("Database created successfully! ✅")