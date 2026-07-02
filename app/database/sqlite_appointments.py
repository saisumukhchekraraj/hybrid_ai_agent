import sqlite3
DATABASE_NAME = "hospital_records.db"
from app.database.sqlite_patients import patient_exists
from app.database.sqlite_docs import doctor_exists
from app.database.sqlite_docs import doc_is_available
def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn
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

    if not doc_is_available(doctor_id, appointment_date, appointment_time):
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
   
    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "Appointment booked successfully.",
        "appointment_id": appointment_id
    }
def cancel_appointment(appointment_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT doctor_id FROM appointment_records WHERE appointment_id = ?
        """,
        (appointment_id,)
    )
    result = cursor.fetchone()

    if result is None:
        conn.close()
        return {
            "success": False,
            "message": "Appointment not found."
        }


    cursor.execute(
        """
        DELETE FROM appointment_records WHERE appointment_id = ?
        """,
        (appointment_id,)
    )


    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "Appointment canceled successfully."
    }
def get_appointments_by_patient(patient_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM appointment_records WHERE patient_id = ?
        """,
        (patient_id,)
    )
    appointments = cursor.fetchall()
    conn.close()

    return [dict(appointment) for appointment in appointments]
def get_appointments_by_doctor(doctor_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM appointment_records WHERE doctor_id = ?
        """,
        (doctor_id,)
    )
    appointments = cursor.fetchall()
    conn.close()

    return [dict(appointment) for appointment in appointments]
def get_appointment(appointment_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM appointment_records WHERE appointment_id = ?
        """,
        (appointment_id,)
    )
    appointment = cursor.fetchone()
    conn.close()

    if appointment:
        return dict(appointment)

    return None



