import csv

from app.data_generator import (
    generate_patient,
    generate_doctor,
    generate_appointment,
    generate_doc_schedule
)
TOTAL_PATIENTS = 100
TOTAL_DOCTORS = 50
TOTAL_APPOINTMENTS = 30

patients = []
for i in range(1, TOTAL_PATIENTS + 1):
    patient = generate_patient(i)
    patients.append(patient)

doctors = []
for i in range(1, TOTAL_DOCTORS + 1):
    doctor = generate_doctor(i)
    doctors.append(doctor)

doctors_schedules=[]
for i in range(1,TOTAL_DOCTORS+1):
    doctor_schedule=generate_doc_schedule(i)
    doctors_schedules.append(doctor_schedule)
appointments=[]
for i in range(1, TOTAL_APPOINTMENTS + 1):
    appointment = generate_appointment(i,TOTAL_PATIENTS,TOTAL_DOCTORS)
    appointments.append(appointment)

with open("data/patients.csv","w",newline="",encoding="utf-8") as file:
    writer = csv.DictWriter(
    file,
    fieldnames=patients[0].keys()
) 
    writer.writeheader()
    writer.writerows(patients)
with open("data/doctors.csv","w",newline="",encoding="utf-8") as file:
    writer = csv.DictWriter(
    file,
    fieldnames=doctors[0].keys()
) 
    writer.writeheader()
    writer.writerows(doctors)
with open("data/doctors_schedules.csv","w",newline="",encoding="utf-8") as file:
    writer=csv.DictWriter(
        file,
        fieldnames=doctors_schedules[0].keys()
    )
    writer.writeheader()
    writer.writerows(doctors_schedules)
with open("data/appointments.csv","w",newline="",encoding="utf-8") as file:
    writer = csv.DictWriter(
    file,
    fieldnames=appointments[0].keys()
) 
    writer.writeheader()
    writer.writerows(appointments)
    

