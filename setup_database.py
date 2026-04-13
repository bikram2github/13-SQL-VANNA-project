
import sqlite3
import random
from datetime import datetime, timedelta

DB_NAME = "clinic.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def drop_tables(cursor):
    cursor.executescript("""
    DROP TABLE IF EXISTS invoices;
    DROP TABLE IF EXISTS treatments;
    DROP TABLE IF EXISTS appointments;
    DROP TABLE IF EXISTS doctors;
    DROP TABLE IF EXISTS patients;
    """)



def create_tables(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        date_of_birth DATE,
        gender TEXT,
        city TEXT,
        registered_date DATE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialization TEXT,
        department TEXT,
        phone TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        doctor_id INTEGER,
        appointment_date DATETIME,
        status TEXT,
        notes TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(id),
        FOREIGN KEY(doctor_id) REFERENCES doctors(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS treatments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        appointment_id INTEGER,
        treatment_name TEXT,
        cost REAL,
        duration_minutes INTEGER,
        FOREIGN KEY(appointment_id) REFERENCES appointments(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        invoice_date DATE,
        total_amount REAL,
        paid_amount REAL,
        status TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(id)
    )
    """)



def generate_basic_data():
    return {
        "first_names": ["Bikram", "Amit", "Rahul", "Priya", "Sneha", "Ravi", "Neha", "Karan", "Anjali"],
        "last_names": ["Maity", "Sharma", "Das", "Singh", "Gupta", "Roy", "Kumar"],
        "cities": ["Kolkata", "Delhi", "Mumbai", "Bangalore","Hyderabad", "Chennai"],
        "genders": ["M", "F"],
        "specializations": ["Dermatology", "Cardiology", "Orthopedics", "General", "Pediatrics"],
        "statuses": ["Scheduled", "Completed", "Cancelled", "No-Show"],
        "invoice_status": ["Paid", "Pending", "Overdue"],
        "treatments": ["X-Ray", "Blood Test", "Skin Therapy", "Physiotherapy"]
    }



def insert_doctors(cursor, data, count=15):
    for _ in range(count):
        name = random.choice(data["first_names"]) + " " + random.choice(data["last_names"])
        spec = random.choice(data["specializations"])
        dept = spec + " Dept"
        phone = f"9{random.randint(100000000,999999999)}"

        cursor.execute("""
        INSERT INTO doctors (name, specialization, department, phone)
        VALUES (?, ?, ?, ?)
        """, (name, spec, dept, phone))


def insert_patients(cursor, data, count=200):
    for i in range(count):
        fname = random.choice(data["first_names"])
        lname = random.choice(data["last_names"])
        email = f"{fname.lower()}{i}@gmail.com"
        phone = f"8{random.randint(100000000,999999999)}"
        dob = datetime.now() - timedelta(days=random.randint(7000, 20000))
        gender = random.choice(data["genders"])
        city = random.choice(data["cities"])
        reg_date = datetime.now() - timedelta(days=random.randint(0, 365))

        cursor.execute("""
        INSERT INTO patients (first_name, last_name, email, phone, date_of_birth, gender, city, registered_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (fname, lname, email, phone, dob.date(), gender, city, reg_date.date()))


def insert_appointments(cursor, data, count=500):
    for _ in range(count):
        patient_id = random.randint(1, 200)
        doctor_id = random.randint(1, 15)
        app_date = datetime.now() - timedelta(days=random.randint(0, 365))
        status = random.choice(data["statuses"])

        cursor.execute("""
        INSERT INTO appointments (patient_id, doctor_id, appointment_date, status, notes)
        VALUES (?, ?, ?, ?, ?)
        """, (patient_id, doctor_id, app_date, status, "Routine check"))


def insert_treatments(cursor, data, count=350):
    for _ in range(count):
        appointment_id = random.randint(1, 500)
        name = random.choice(data["treatments"])
        cost = random.randint(50, 5000)
        duration = random.randint(10, 120)

        cursor.execute("""
        INSERT INTO treatments (appointment_id, treatment_name, cost, duration_minutes)
        VALUES (?, ?, ?, ?)
        """, (appointment_id, name, cost, duration))


def insert_invoices(cursor, data, count=300):
    for _ in range(count):
        patient_id = random.randint(1, 200)
        total = random.randint(100, 10000)
        paid = random.randint(0, total)
        status = random.choice(data["invoice_status"])
        date = datetime.now() - timedelta(days=random.randint(0, 365))

        cursor.execute("""
        INSERT INTO invoices (patient_id, invoice_date, total_amount, paid_amount, status)
        VALUES (?, ?, ?, ?, ?)
        """, (patient_id, date.date(), total, paid, status))


def main():
    conn = get_connection()
    cursor = conn.cursor()

    data = generate_basic_data()

    #drop_tables(cursor)
    create_tables(cursor)

    insert_doctors(cursor, data)
    insert_patients(cursor, data)
    insert_appointments(cursor, data)
    insert_treatments(cursor, data)
    insert_invoices(cursor, data)

    conn.commit()
    conn.close()

    print("Database setup completed successfully!")


if __name__ == "__main__":
    main()