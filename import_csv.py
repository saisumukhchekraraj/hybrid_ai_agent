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
                insurance_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
        (row["patient_id"],row["first_name"],row["last_name"],
         row["dob"],row["gender"],row["phone"],row["email"],
         row["address"],row["insurance_company"],row["insurance_id"]
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
                    doc_name,
                    department,
                    specialty,
                    day_of_week,
                    time_slot,
                    is_available
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (row["doc_name"], row["department"], row["specialty"],
                 row["day_of_week"], row["time_slot"], row["is_available"])
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