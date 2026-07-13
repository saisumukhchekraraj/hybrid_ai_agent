import streamlit as st
import pandas as pd
from pathlib import Path
import requests
REPORT_FILE = Path("admin_review_report.xlsx")
BASE_URL = "http://127.0.0.1:8000"
def get_appointment_details(appointment_id: int) -> dict:
    """
    Fetch appointment details from FastAPI.
    """

    response = requests.get(
        f"{BASE_URL}/appointments/{appointment_id}"
    )

    response.raise_for_status()

    return response.json()
def get_patient_details(patient_id: int) -> dict:
    """
    Fetch patient details from FastAPI.
    """

    response = requests.get(
        f"{BASE_URL}/patients/{patient_id}"
    )

    response.raise_for_status()

    return response.json()
def get_doctor_details(doctor_id: int) -> dict:
    """
    Fetch doctor details from FastAPI.
    """

    response = requests.get(
        f"{BASE_URL}/doctors/{doctor_id}"
    )

    response.raise_for_status()

    return response.json()

def export_booking_to_excel(
    appointment: dict,
    patient: dict,
    doctor: dict , email: str | None = None
):
    """
    Export booking details to an Excel file.
    """

    # Create a DataFrame with the appointment and patient details

    booking_record = {
        "Appointment ID": appointment["appointment_id"],
        "Patient ID": patient["patient_id"],
        "Patient Name": f"{patient['first_name']} {patient['last_name']}",
        "Email": patient.get("email") or email or "Email not provided",
        "Insurance Company": [patient["insurance_company"]],
        "Insurance ID": [patient["insurance_id"]],
        "Appointment Date": [appointment["appointment_date"]],
        "Appointment Time": [appointment["appointment_time"]],
        "Doctor ID": [appointment["doctor_id"]],
        "Doctor Name": [doctor["doc_name"]],
        "Specialty": [doctor["specialty"]]
    }
    new_booking = pd.DataFrame([booking_record])
    if REPORT_FILE.exists():
        # If the report file exists, append the new booking to it
        existing_report = pd.read_excel(REPORT_FILE)
        updated_report = pd.concat([existing_report, new_booking], ignore_index=True)
        updated_report.to_excel(REPORT_FILE, index=False)
    else:
        # If the report file doesn't exist, create a new one with the new booking
        new_booking.to_excel(REPORT_FILE, index=False)

def send_dummy_email(patient: dict , email: str | None = None):
    """
    Simulates sending a patient intake form email.
    """

    patient_name = (
        f"{patient['first_name']} {patient['last_name']}"
    )

    patient_email = patient.get("email") or email or "Email not provided"

    print("\n" + "=" * 50)
    print("📧 EMAIL AUTOMATION")
    print("=" * 50)
    print(f"Recipient : {patient_name}")
    print(f"Email     : {patient_email}")
    print("Subject   : Patient Intake Form")
    print()
    print(f"Sending patient intake form to {patient_email}...")
    print("Status    : SUCCESS")
    print("=" * 50)
def get_email() -> str | None:
    """
    Retrieves the user's email from the session state.
    """

    return st.session_state.get("user_email")
def process_booking(appointment_id: int ):
    """
    Executes all post-booking automation.
    """
    email = get_email()
    appointment = get_appointment_details(appointment_id)

    patient = get_patient_details(
        appointment["patient_id"]
    )

    doctor = get_doctor_details(
        appointment["doctor_id"]
    )

    export_booking_to_excel(
        appointment,
        patient,doctor , email
    )

    send_dummy_email(
        patient , email
    )