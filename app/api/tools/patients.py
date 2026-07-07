from langchain_core.tools import tool
import requests

@tool
def lookup_patient(first_name: str, last_name: str, dob: str):
    """
Call this tool to check if a patient exists in the hospital database.


""" 
    response = requests.post(
    "http://127.0.0.1:8000/patients/lookup",
    json={
        "first_name": first_name,
        "last_name": last_name,
        "dob": dob
    },timeout=10)
    response.raise_for_status()
    return response.json()
@tool
def create_patient(
    first_name: str,
    last_name: str,
    dob: str,
    gender: str
):
    """

Create a new patient record.

Only use this tool after lookup_patient has confirmed
that no matching patient exists.

Never use this tool to update an existing patient.

"""
    response = requests.post(
    "http://127.0.0.1:8000/patients/new",
    json={
        "first_name": first_name,
        "last_name": last_name,
        "dob": dob,
        "gender": gender
    },timeout=10)
    response.raise_for_status()
    return response.json()
@tool
def get_doctor_availability(department: str, appointment_date: str , duration: int | None = None):
    """ Call this tool to get the available doctor slots for a specific department on a given date."""
    response = requests.post(
    "http://127.0.0.1:8000/doctors/availability",
    json={
        "department": department,
        "appointment_date": appointment_date,
        "duration": duration
    },timeout=10)
    response.raise_for_status()
    return response.json()
@tool
def book_appointment(patient_id: int, doctor_id: int, appointment_date: str, appointment_time: str):
    """ Call this tool to book an appointment for a patient with a specific doctor on a given date and time.
    Always check doctor availability before booking an appointment.
    Always check if the patient exists before booking an appointment.
    If the patient does not exist, use the create_patient tool to create a new patient record first."""
    response = requests.post(
    "http://127.0.0.1:8000/appointments/book",
    json={
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "appointment_date": appointment_date,
        "appointment_time": appointment_time
    },timeout=10)
    response.raise_for_status()
    return response.json()
