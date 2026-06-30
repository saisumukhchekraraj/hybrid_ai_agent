import sqlite3
DATABASE_NAME = "hospital_records.db"

from hybrid_ai_agent.app.database.sqlite_patients import patient_exists
def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patient_records (
            
            patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            dob TEXT,
            gender TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            insurance_company TEXT,
            insurance_id TEXT
        )
    ''')
    cursor.execute("""
                  CREATE TABLE IF NOT EXISTS doctor_records (
                      doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                      doc_name TEXT,
                      department TEXT,
                      specialty TEXT,
                      qualifications TEXT,
                      phone TEXT,
                      email TEXT,
                      consultation_fee REAL
                  )
 """)
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS doctor_schedule (
                       schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       doctor_id INTEGER,
                       day_of_week TEXT,
                       start_time TEXT,
                       end_time TEXT,
                       duration_minutes INTEGER,
                       FOREIGN KEY (doctor_id) REFERENCES doctor_records(doctor_id)
                   )
 """)
    cursor.execute("""
                  CREATE TABLE IF NOT EXISTS appointment_records (
                      appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                      patient_id INTEGER,
                      doctor_id INTEGER,
                      appointment_date TEXT,
                      appointment_time TEXT,
                      appointment_status TEXT,
                      FOREIGN KEY (patient_id) REFERENCES patient_records(patient_id),
                      FOREIGN KEY (doctor_id) REFERENCES doctor_records(doctor_id)
                  )""")
    conn.commit()
    conn.close()



def book_appointment(
    patient_id,
    doctor_id,
    appointment_date,
    appointment_time
):
   
    if not patient_exists(patient_id):
        return {
            "success": False,
            "message": "Patient not found."
        }

    doctor = doctor_exists(doctor_id)

    if doctor is None:
        return {
            "success": False,
            "message": "Doctor not found."
        }

    if not doctor["is_available"]:
        return {
            "success": False,
            "message": "Doctor not available."
        }
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO appointment_records
        (
            patient_id,
            doctor_id,
            appointment_date,
            appointment_time,
            appointment_status
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            patient_id,
            doctor_id,
            appointment_date,
            appointment_time,
            "Scheduled"
        )
    )
    appointment_id = cursor.lastrowid
    cursor.execute(
        """
        UPDATE doctor_records
        SET is_available = 0
        WHERE doctor_id = ?
        """,
        (doctor_id,)
    )

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "Appointment booked successfully.",
        "appointment_id": appointment_id
    }

   

