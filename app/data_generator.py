from faker import Faker
import random
from datetime import date
from app.hugging_face import generate_complaint
fake = Faker("en_IN")
today= date.today()
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
DAYS=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
START_TIMES = [
    "08:00",
    "08:30",
    "09:00",
    "09:30",
    "10:00",
    "10:30",
    "11:00"
]

END_TIMES = [
    "15:00",
    "16:00",
    "17:00",
    "18:00",
    "19:00"
]
doctor_qualifications = [
    "MBBS",
    "MBBS, MD",
    "MBBS, MS",
    "MBBS, DNB",
    "MBBS, MD (General Medicine)",
    "MBBS, MD (Cardiology)",
    "MBBS, DM (Cardiology)",
    "MBBS, MD (Neurology)",
    "MBBS, DM (Neurology)",
    "MBBS, MS (Orthopedics)",
    "MBBS, MS (General Surgery)",
    "MBBS, MCh (Neurosurgery)",
    "MBBS, MCh (Urology)",
    "MBBS, MD (Pediatrics)",
    "MBBS, MD (Dermatology)",
    "MBBS, MD (Psychiatry)",
    "MBBS, MD (Radiology)",
    "MBBS, MD (Anesthesiology)",
    "MBBS, MD (Ophthalmology)",
    "MBBS, MS (ENT)",
    "MBBS, MD (Pulmonology)",
    "MBBS, DM (Gastroenterology)",
    "MBBS, MD (Nephrology)",
    "MBBS, DM (Endocrinology)",
    "MBBS, MD (Oncology)",
    "MBBS, MD (Emergency Medicine)",
    "MBBS, MD (Obstetrics & Gynecology)",
    "MBBS, MD (Pathology)",
    "MBBS, MD (Microbiology)",
    "MBBS, MD (Community Medicine)"
]
DURATIONS = [30,60]
def generate_patient(patient_number): 
    """Generates a random patient record."""
    
    patient_id= patient_number
   
    date_of_birth=fake.date_of_birth(minimum_age=0, maximum_age=90)
    dob=date_of_birth.strftime("%Y-%m-%d")
    age = today.year - date_of_birth.year - (
    (today.month, today.day) < (date_of_birth.month, date_of_birth.day)
)
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
    complaint= generate_complaint(age, gender)
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
        "insurance_id": insurance_id,
        "patient_complaint": complaint
    }
    return patient

def generate_doctor(doctor_number):
    """Generates a random doctor record."""
    doctor_id = doctor_number
    doc_name = f"Dr.{fake.first_name()} {fake.last_name()}"
    department = random.choice(DEPARTMENTS)
    specialty = SPECIALITIES[department]
    qualifications= random.choice(doctor_qualifications)
    email=fake.unique.email()
    phone=fake.phone_number()
    doctor= {
        "doctor_id": doctor_id,
        "doc_name": doc_name,
        "department": department,
        "specialty": specialty,
        "qualifications":qualifications,
        "email":email,
        "phone":phone,
    }
    return doctor
import random

def generate_doc_schedule(doctor_id):
    day_of_week = random.choice(DAYS)
    start_time = random.choice(START_TIMES)
    valid_end_times = [
        end
        for end in END_TIMES
        if end > start_time
    ]
    end_time = random.choice(valid_end_times)
    duration_minutes = random.choice(DURATIONS)
    return {
        "doctor_id": doctor_id,
        "day_of_week": day_of_week,
        "start_time": start_time,
        "end_time": end_time,
        "duration_minutes": duration_minutes
    }
def generate_appointment(appointment_number, total_patients, total_doctors):
    """Generates a random appointment record."""
    appointment_id = appointment_number
    appointment_date = fake.date_between(start_date="today", end_date="+30d").strftime("%Y-%m-%d")
    appointment_time = f"{random.randint(8, 16):02d}:00"
    appointment_status = random.choice(["Scheduled", "Completed"])
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