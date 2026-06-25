import sqlite3
DATABASE_NAME = "hospital_records.db"


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
                      day_of_week TEXT,
                      time_slot TEXT,
                      is_available BOOLEAN
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
def find_patient(first_name, last_name, dob):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
    """
    SELECT patient_id
    FROM patient_records
    WHERE
        first_name = ?
        AND last_name = ?
        AND dob = ?
    LIMIT 1
    """,
    (first_name, last_name, dob)
)
    patient = cursor.fetchone()
    conn.close()
    if patient:
     return patient["patient_id"]

    return None
def insert_patient(
    first_name,
    last_name,
    dob,
    gender,
    phone,
    email,
    address,
    insurance_company,
    insurance_id
): 
   patient_id = find_patient(first_name, last_name, dob)

   if patient_id:
    return patient_id
   else:
    conn= get_connection()
    cursor=conn.cursor()
    cursor.execute("""
       INSERT  INTO patient_records
    (
        first_name,
        last_name,
        dob,
        gender,
        phone,
        email,
        address,
        insurance_company,
        insurance_id
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        first_name,
        last_name,
        dob,
        gender,
        phone,
        email,
        address,
        insurance_company,
        insurance_id
    )
)
    conn.commit()
    patient_id = cursor.lastrowid
    conn.close()
    return patient_id
def get_available_doctors(specialty, day):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            doctor_id,
            doc_name,
            specialty,
            day_of_week,
            time_slot
        FROM doctor_records
        WHERE
            specialty = ?
            AND day_of_week = ?
            AND is_available = 1
        """,
        (specialty, day)
    )

    doctors = cursor.fetchall()

    conn.close()

    return [dict(doctor) for doctor in doctors]

   

