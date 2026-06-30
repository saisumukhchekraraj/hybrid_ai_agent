import sqlite3
DATABASE_NAME = "hospital_records.db"
def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn
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

def doctor_exists(doctor_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            doctor_id,
            is_available
        FROM doctor_records
        WHERE doctor_id = ?
        LIMIT 1
        """,
        (doctor_id,)
    )

    doctor = cursor.fetchone()

    conn.close()

    return doctor