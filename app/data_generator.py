from faker import Faker
import random

fake = Faker("en_IN")

DEPARTMENTS = [
    "Cardiology",
    "Neurology",
    "Orthopedics",
    "Dermatology",
    "ENT",
    "Pediatrics",
    "Pulmonology",
    "General Medicine"
]

INSURANCE_COMPANIES = [
    "Star Health",
    "Niva Bupa",
    "ICICI Lombard",
    "HDFC ERGO",
    "Care Health"
]

SPECIALITIES = {
    "Cardiology": "Cardiologist",
    "Neurology": "Neurologist",
    "Orthopedics": "Orthopedic Surgeon",
    "Dermatology": "Dermatologist",
    "ENT": "ENT Specialist",
    "Pediatrics": "Pediatrician",
    "Pulmonology": "Pulmonologist",
    "General Medicine": "General Physician"
}
TIME_SLOTS = [
    "09:00-10:00",
    "10:00-11:00",
    "11:00-12:00",
    "14:00-15:00",
    "15:00-16:00"
]
def generate_patient(patient_number): 
    """Generates a random patient record."""
    
    patient_id= patient_number
   
    dob=fake.date_of_birth(minimum_age=0, maximum_age=90).strftime("%m/%d/%Y")
    gender=random.choice(["male", "female"])
    if gender == "male":
        first_name = fake.first_name_male()
        last_name = fake.last_name()
    else:
        first_name = fake.first_name_female()
        last_name = fake.last_name()
    phone=fake.phone_number()
    email=fake.unique.email()
    address=fake.address().replace("\n", ", ")
    insurance_company=random.choice(INSURANCE_COMPANIES)
    insurance_id=fake.bothify(text="??-??####").upper()
    patient = { 
        
        "patient_id": patient_id,
        "first_name": first_name,
        "last_name": last_name,
        "dob": dob,
        "gender": gender,
        "phone": phone,
        "email": email,
        "address": address,
        "insurance_company": insurance_company,
        "insurance_id": insurance_id
    }
    return patient
def generate_doctor(doctor_number):
    """Generates a random doctor record."""
    doctor_id = doctor_number
    doc_name = f"Dr.{fake.first_name()} {fake.last_name()}"
   
    department = random.choice(DEPARTMENTS)
    specialty = SPECIALITIES[department]
    day_of_week = random.choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday","Saturday"])
 

    time_slot = random.choice(TIME_SLOTS)
    is_available = random.choice([True, False])
    doctor= {
        "doctor_id": doctor_id,
        "doc_name": doc_name,
        "department": department,
        "specialty": specialty,
        "day_of_week": day_of_week,
        "time_slot": time_slot,
        "is_available": is_available
    }
    return doctor

def generate_appointment(appointment_number, total_patients, total_doctors):
    """Generates a random appointment record."""
    appointment_id = appointment_number
    appointment_date = fake.date_between(start_date="today", end_date="+30d").strftime("%Y-%m-%d")
    appointment_time = f"{random.randint(8, 16)}:00"
    appointment_status = random.choice(["Scheduled", "Completed", "Cancelled"])
    appointment_record = {
        "appointment_id": appointment_id,
        "patient_id": random.randint(1, total_patients),
        "doctor_id": random.randint(1, total_doctors),
        "appointment_date": appointment_date,
        "appointment_time": appointment_time,
        "appointment_status": appointment_status
    }
    return appointment_record
if __name__ == "__main__":
    print(generate_patient(1))
    print()
    print(generate_doctor(1))
    print()
    print(generate_appointment(1, 1000, 100))