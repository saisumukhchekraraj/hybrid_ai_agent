import sqlite3
DATABASE_NAME = "hospital_records.db"
def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn
#--------------------------------
#Doctor-related functions
#--------------------------------
def get_all_doctors():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            doctor_id,
            doc_name,
            department,
            specialty,
            qualifications,
            phone,
            email
        FROM doctor_records
        """
    )

    doctors = cursor.fetchall()

    conn.close()

    return [dict(doctor) for doctor in doctors]

def update_doctor_info(doctor_id, doc_name=None, department=None, specialty=None, qualifications=None, phone=None, email=None):
    conn = get_connection()
    cursor = conn.cursor()

    update_fields = []
    update_values = []

    if doc_name is not None:
        update_fields.append("doc_name = ?")
        update_values.append(doc_name)
    if department is not None:
        update_fields.append("department = ?")
        update_values.append(department)
    if specialty is not None:
        update_fields.append("specialty = ?")
        update_values.append(specialty)
    if qualifications is not None:
        update_fields.append("qualifications = ?")
        update_values.append(qualifications)
    if phone is not None:
        update_fields.append("phone = ?")
        update_values.append(phone)
    if email is not None:
        update_fields.append("email = ?")
        update_values.append(email)

    if update_fields:
        update_query = f"""
            UPDATE doctor_records
            SET {', '.join(update_fields)}
            WHERE doctor_id = ?
        """
        update_values.append(doctor_id) 
        cursor.execute(update_query, tuple(update_values))
        conn.commit()

    conn.close()
def get_doctor(doctor_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM doctor_records
        WHERE doctor_id = ?
        LIMIT 1
        """,
        (doctor_id,)
    )

    doctor = cursor.fetchone()

    conn.close()

    if doctor:
        return dict(doctor)

    return None


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
#------------------------------------------
#doctor Schedule and availability functions
#------------------------------------------
def get_doctor_schedule(doctor_id , day_of_week=None):
    conn = get_connection()
    cursor = conn.cursor()
    if day_of_week:
        cursor.execute(
            """
            SELECT *
            FROM doctor_schedule
            WHERE doctor_id = ? AND day_of_week = ?
            """,
            (doctor_id, day_of_week)
        )
    else:
        cursor.execute(
            """
            SELECT *
            FROM doctor_schedule
            WHERE doctor_id = ?
            """,
            (doctor_id,)
        )
    schedule = cursor.fetchall()
    conn.close()
    return [dict(entry) for entry in schedule]
def update_doctor_schedule(doctor_id, day_of_week, start_time, end_time, duration_minutes=None):
    conn = get_connection()
    cursor = conn.cursor()
    exists = cursor.execute("""
                            SELECT schedule_id FROM doctor_schedule WHERE doctor_id = ? AND day_of_week = ?
                            """, (doctor_id, day_of_week)).fetchone()
    if exists:
        if duration_minutes is not None:
            cursor.execute("""
                            UPDATE doctor_schedule
                            SET start_time = ?, end_time = ?, duration_minutes = ?
                            WHERE doctor_id = ? AND day_of_week = ?
                            """, (start_time, end_time, duration_minutes, doctor_id, day_of_week))
        else:
            cursor.execute("""
                            UPDATE doctor_schedule
                            SET start_time = ?, end_time = ?
                            WHERE doctor_id = ? AND day_of_week = ?
                            """, (start_time, end_time, doctor_id, day_of_week))
    else:
        if duration_minutes is not None:
            cursor.execute("""
                            INSERT INTO doctor_schedule (doctor_id, day_of_week, start_time, end_time, duration_minutes)
                            VALUES (?, ?, ?, ?, ?)
                            """, (doctor_id, day_of_week, start_time, end_time, duration_minutes))
        else:
            cursor.execute("""
                            INSERT INTO doctor_schedule (doctor_id, day_of_week, start_time, end_time)
                            VALUES (?, ?, ?, ?)
                            """, (doctor_id, day_of_week, start_time, end_time))
    conn.commit()
    conn.close()
def delete_doctor_schedule(doctor_id, day_of_week):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                    DELETE FROM doctor_schedule
                    WHERE doctor_id = ? AND day_of_week = ?
                    """, (doctor_id, day_of_week))
    conn.commit()
    rows= cursor.rowcount
    conn.close()
    return rows > 0
#-----------------------------------------------------
#Doctor availability and appointment slot functions
#-----------------------------------------------------
def get_weekday_slots(doctor_id, day_of_week):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT start_time, end_time, duration_minutes
        FROM doctor_schedule
        WHERE doctor_id = ? AND day_of_week = ?
        """,
        (doctor_id, day_of_week)
    )

    schedule = cursor.fetchone()

    if not schedule:
        conn.close()
        return []

    start_time = schedule["start_time"]
    end_time = schedule["end_time"]
    duration_minutes = schedule["duration_minutes"]

    # Generate time slots based on the schedule
    slots = []
    start_time_minutes = int(start_time.split(":")[0]) * 60 + int(start_time.split(":")[1])
    end_time_minutes = int(end_time.split(":")[0]) * 60 + int(end_time.split(":")[1])
    current_time_minutes = start_time_minutes
    while current_time_minutes + duration_minutes <= end_time_minutes:
        slot_start = f"{current_time_minutes // 60:02}:{current_time_minutes % 60:02}"
        slot_end = f"{(current_time_minutes + duration_minutes) // 60:02}:{(current_time_minutes + duration_minutes) % 60:02}"
        slots.append({"start_time": slot_start, "end_time": slot_end})
        current_time_minutes += duration_minutes
    return slots

def get_available_doctor_slots(specialty, date):
    day = date.strftime("%A")  
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
        d.doctor_id,
        d.doc_name,
        s.start_time,
        s.end_time,
        s.slot_duration
        FROM doctor_records d
        JOIN doctor_schedule s
        ON d.doctor_id = s.doctor_id
        WHERE d.specialty = ?
        AND s.weekday = ?
            """, (specialty, day))
    doctors = cursor.fetchall()

    doc_slots = []
    for doctor in doctors:
        doctor_id = doctor["doctor_id"]
        slots = get_weekday_slots(doctor_id, day)
        
        cursor.execute(""" 
            SELECT appointment_time
            FROM appointment_records
            WHERE doctor_id = ? AND appointment_date = ?
        """, (doctor_id, date.strftime("%Y-%m-%d")))
        appointments = cursor.fetchall()
        available_slots = slots.copy()  

        for appointment in appointments:
            appointment_time = appointment["appointment_time"]
            available_slots = [slot for slot in available_slots if slot["start_time"] != appointment_time]

        slot_list = []
        for slot in available_slots:
              slot_list.append({
              "start": slot["start_time"],
              "end": slot["end_time"]
          })
        doctor_data = {
             "doctor_id": doctor["doctor_id"],
             "doc_name": doctor["doc_name"],
             "available_slots": slot_list
} 
        doc_slots.append(doctor_data)
    conn.close()        
    return doc_slots
