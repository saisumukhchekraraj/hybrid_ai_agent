import sqlite3
DATABASE_NAME = "patients.db"

def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

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
def get_patient(patient_id):
    if(not patient_exists(patient_id)):
        return None
    else:
     conn = get_connection()
     cursor = conn.cursor()

     cursor.execute(
        """
        SELECT *
        FROM patient_records
        WHERE patient_id = ?
        LIMIT 1
        """,
        (patient_id,)
    )

     patient = cursor.fetchone()

     conn.close()

     if patient:
        return dict(patient)

     return None
def update_patient_info(
    patient_id,
    first_name=None,
    last_name=None,
    dob=None,
    gender=None,
    phone=None,
    email=None,
    address=None,
    insurance_company=None,
    insurance_id=None
): 
    conn = get_connection()
    cursor = conn.cursor()

    # Build the SET clause dynamically based on provided arguments
    set_clause = []
    values = []

    if first_name is not None:
        set_clause.append("first_name = ?")
        values.append(first_name)

    if last_name is not None:
        set_clause.append("last_name = ?")
        values.append(last_name)

    if dob is not None:
        set_clause.append("dob = ?")
        values.append(dob)

    if gender is not None:
        set_clause.append("gender = ?")
        values.append(gender)

    if phone is not None:
        set_clause.append("phone = ?")
        values.append(phone)

    if email is not None:
        set_clause.append("email = ?")
        values.append(email)

    if address is not None:
        set_clause.append("address = ?")
        values.append(address)

    if insurance_company is not None:
        set_clause.append("insurance_company = ?")
        values.append(insurance_company)

    if insurance_id is not None:
        set_clause.append("insurance_id = ?")
        values.append(insurance_id)

    if not set_clause:
        conn.close()
        return False

    # Construct the final query
    query = f"UPDATE patient_records SET {', '.join(set_clause)} WHERE patient_id = ?"
    values.append(patient_id)

    cursor.execute(query, values)
    conn.commit()
    conn.close()

    return True

def delete_patient(patient_id):
    conn = get_connection()
    cursor= conn.cursor()
    cursor.execute(
        """ 
         DELETE FROM patient_records
         WHERE patient_id = ?
         """, (patient_id,))
    conn.commit()
    conn.close()
def patient_exists(patient_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT patient_id
        FROM patient_records
        WHERE patient_id = ?
        LIMIT 1
        """,
        (patient_id,)
    )

    patient = cursor.fetchone()

    conn.close()

    if patient:
        return True

    return False