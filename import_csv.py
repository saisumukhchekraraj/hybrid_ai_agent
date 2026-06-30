import csv
from app.database.sqlite import get_connection,create_tables
create_tables()

def import_patients():

  conn = get_connection()
  cursor = conn.cursor()
  with open(
    "data/patients.csv",
    "r",
    encoding="utf-8"
) as file:
    reader = csv.DictReader(file)
    for row in reader:
        cursor.execute(
            """
            INSERT INTO patient_records (
                patient_id,
                first_name,
                last_name,
                dob,
                gender,
                phone,
                email,
                address,
                insurance_company,
                insurance_id,
                patient_complaint
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
        (row["patient_id"],row["first_name"],row["last_name"],
         row["dob"],row["gender"],row["phone"],row["email"],
         row["address"],row["insurance_company"],row["insurance_id"],row["patient_complaint"]
) )
    conn.commit()
    conn.close()
def import_doctors():
    conn = get_connection()
    cursor = conn.cursor()
    with open(
        "data/doctors.csv",
        "r",
        encoding="utf-8"
    ) as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute(
                """
                INSERT INTO doctor_records (
                    doctor_id,
                    doc_name,
                    department,
                    specialty,
                    qualifications,
                    phone,
                    email
                ) VALUES (?,?, ?, ?, ?, ?, ?)
                """,
                (row["doctor_id"],row["doc_name"], row["department"], row["specialty"],
                 row["qualifications"], row["phone"], row["email"])
            )
        conn.commit()
        conn.close()
def import_doctor_schedules():
    conn = get_connection()
    cursor = conn.cursor()

    with open(
        "data/doctor_schedule.csv",
        "r",
        encoding="utf-8"
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            cursor.execute(
                """
                INSERT INTO doctor_schedule (
                    doctor_id,
                    day_of_week,
                    start_time,
                    end_time,
                    duration_minutes
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    row["doctor_id"],
                    row["day_of_week"],
                    row["start_time"],
                    row["end_time"],
                    row["duration_minutes"]
                )
            )

    conn.commit()
    conn.close()
def import_appointments():
    conn = get_connection()
    cursor = conn.cursor()
    with open(
        "data/appointments.csv",
        "r",
        encoding="utf-8"
    ) as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute(
                """
                INSERT INTO appointment_records (
                    patient_id,
                    doctor_id,
                    appointment_date,
                    appointment_time,
                    appointment_status
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (row["patient_id"], row["doctor_id"], row["appointment_date"],
                 row["appointment_time"], row["appointment_status"])
            )
        conn.commit()
        conn.close()
if __name__ == "__main__":
    import_patients()
    import_doctors()
    import_appointments()
    print("Data imported successfully.")