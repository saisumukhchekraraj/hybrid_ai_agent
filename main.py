from fastapi import FastAPI
from pydantic import BaseModel
from pydantic import BaseModel
from typing import Optional
from datetime import date
from app.database.sqlite_patients import(
    insert_patient,
    update_patient_info,
    delete_patient,
    patient_exists,
    get_patient,
    find_patient
)
from app.database.sqlite_docs import(
    get_all_doctors,
    update_doctor_info,
    get_doctor,
    get_doctor_schedule,
    update_doctor_schedule,
    get_available_doctor_slots
)
from app.database.sqlite_appointments import (
    book_appointment,
    cancel_appointment,
    get_appointment,
    get_appointments_by_patient,
    get_appointments_by_doctor
)
app = FastAPI()


class NewPatient(BaseModel):
    first_name: str
    last_name: str
    dob: str
    gender: str
    phone: str
    email: str
    address: str
    insurance_company: str
    insurance_id: str

class UpdatePatient(BaseModel):
    patient_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    dob: Optional[str] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    insurance_company: Optional[str] = None
    insurance_id: Optional[str] = None
class PatientLookupRequest(BaseModel):
    first_name: str
    last_name: str
    dob: str

class UpdateDoctorInfo(BaseModel):
    doctor_id: int
    doc_name: str | None = None
    department: str | None = None
    specialty: str | None = None
    qualifications: str | None = None
    phone: str | None = None
    email: str | None = None

class UpdateDoctorSchedule(BaseModel):
    doctor_id: int
    day_of_week: str
    start_time: str
    end_time: str
    duration_minutes: int | None = None

class DoctorAvailabilityRequest(BaseModel):
    department: str
    appointment_date: str
    
class BookAppointmentRequest(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: str
    appointment_time: str

#===========
#home
#===========
@app.get("/")
def home():

    return {
        "message": "Hybrid AI Hospital API is running."
    }
#-----------------------------------
#patients routes
#-----------------------------------
@app.post("/patients/lookup")
def patient_lookup(patient: PatientLookupRequest):

    patient_id = find_patient(
        patient.first_name,
        patient.last_name,
        patient.dob
    )

    if patient_id:

        return {
            "status": "returning",
            "patient_id": patient_id
        }

    return {
        "status": "new",
        "patient_id": None
    }
@app.post("/patients/new")
def create_patient_route(request: NewPatient):

    patient_id = insert_patient(
        first_name=request.first_name,
        last_name=request.last_name,
        dob=request.dob,
        gender=request.gender,
        phone=request.phone,
        email=request.email,
        address=request.address,
        insurance_company=request.insurance_company,
        insurance_id=request.insurance_id
    )

    return {
        "message": "Patient created successfully",
        "patient_id": patient_id
    }
@app.put("/patients/change")
def update_patient_route(request: UpdatePatient):

    rows_updated = update_patient_info(
        patient_id=request.patient_id,
        first_name=request.first_name,
        last_name=request.last_name,
        dob=request.dob,
        gender=request.gender,
        phone=request.phone,
        email=request.email,
        address=request.address,
        insurance_company=request.insurance_company,
        insurance_id=request.insurance_id
    )

    if rows_updated == 0:
        return {
            "message": "Patient not found"
        }

    return {
        "message": "Patient updated successfully"
    }
@app.get("/patients/{patient_id}")
def get_patient_route(patient_id: int):

    patient = get_patient(patient_id)

    if patient is None:
        return {
            "message": "Patient not found"
        }

    return patient
@app.delete("/patients/{patient_id}")
def delete_patient_route(patient_id: int):

    rows_deleted = delete_patient(patient_id)

    if rows_deleted == 0:
        return {
            "message": "Patient not found"
        }

    return {
        "message": "Patient deleted successfully"
    }
#-----------------------------
#doctors routes
#-----------------------------
@app.get("/doctors")
def get_all_doctors_route():
    return get_all_doctors()

@app.get("/doctors/{doctor_id}")
def get_doctor_route(doctor_id: int):

    doctor = get_doctor(doctor_id)

    if doctor is None:
        return {"message": "Doctor not found"}

    return doctor

@app.put("/doctors/update")
def update_doctor_info_route(request: UpdateDoctorInfo):

    update_doctor_info(
        doctor_id=request.doctor_id,
        doc_name=request.doc_name,
        department=request.department,
        specialty=request.specialty,
        qualifications=request.qualifications,
        phone=request.phone,
        email=request.email
    )

    return {
        "message": "Doctor information updated successfully"
    }
@app.get("/doctors/{doctor_id}/schedule")
def get_doctor_schedule_route(
    doctor_id: int,
    day_of_week: str | None = None
):

    return get_doctor_schedule(
        doctor_id=doctor_id,
        day_of_week=day_of_week
    )

@app.put("/doctors/schedule")
def update_doctor_schedule_route(request: UpdateDoctorSchedule):

    update_doctor_schedule(
        doctor_id=request.doctor_id,
        day_of_week=request.day_of_week,
        start_time=request.start_time,
        end_time=request.end_time,
        duration_minutes=request.duration_minutes
    )

    return {
        "message": "Doctor schedule updated successfully"
    }

@app.post("/doctors/availability")
def doctor_availability_route(request: DoctorAvailabilityRequest):

    return get_available_doctor_slots(
        department=request.department,
        date=request.appointment_date
    )

#-------------------
#appointments routes
#-------------------
@app.post("/appointments/book")
def book_appointment_route(request: BookAppointmentRequest):
     
       return book_appointment(
        patient_id=request.patient_id,
        doctor_id=request.doctor_id,
        appointment_date=request.appointment_date,
        appointment_time=request.appointment_time
    )

@app.delete("/appointments/{appointment_id}")
def cancel_appointment_route(appointment_id: int):

    return cancel_appointment(appointment_id)

@app.get("/appointments/{appointment_id}")
def get_appointment_route(appointment_id: int):

    appointment = get_appointment(appointment_id)

    if appointment is None:
        return {
            "message": "Appointment not found"
        }

    return appointment

@app.get("/appointments/patient/{patient_id}")
def get_patient_appointments_route(patient_id: int):

    return get_appointments_by_patient(patient_id)

@app.get("/appointments/doctor/{doctor_id}")
def get_doctor_appointments_route(doctor_id: int):

    return get_appointments_by_doctor(doctor_id)