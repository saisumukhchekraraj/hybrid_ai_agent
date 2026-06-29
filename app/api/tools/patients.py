from langchain_core.tools import tool
import requests

@tool
def lookup_patient(first_name: str, last_name: str, dob: str):
    """
Call this tool to check if a patient exists in the hospital database.

Always use this tool when the user provides
their name and date of birth.
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