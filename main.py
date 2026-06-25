from fastapi import FastAPI
from pydantic import BaseModel

from app.database.sqlite import (
    find_patient,
    get_available_doctors,
    book_appointment
)

app = FastAPI()
class PatientLookupRequest(BaseModel):
    first_name: str
    last_name: str
    dob: str


class DoctorAvailabilityRequest(BaseModel):
    specialty: str
    day: str
    


class AppointmentBookingRequest(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: str
    appointment_time: str
@app.get("/")
def home():

    return {
        "message": "Hybrid AI Hospital API is running."
    }
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
@app.post("/doctors/availability")
def doctor_availability(request: DoctorAvailabilityRequest):

    doctors = get_available_doctors(
        request.specialty,
        request.day
    )

    return doctors
@app.post("/appointments/book")
def appointment_booking(request: AppointmentBookingRequest):

    return book_appointment(
        request.patient_id,
        request.doctor_id,
        request.appointment_date,
        request.appointment_time
    )