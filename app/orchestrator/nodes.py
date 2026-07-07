from app.api.tools.patients import book_appointment, lookup_patient
from app.orchestrator.state import AgentState
from app.api.tools.patients import get_doctor_availability
from app.api.language_chain import llm_with_tools
from langchain_core.messages import AIMessage
from langgraph.prebuilt import ToolNode
def duration_node(state: AgentState) -> dict:
    """
    Determine the appointment duration based on patient status.

    Business Rule:
    - New patient -> 60 minutes
    - Returning patient -> 30 minutes
    """

    if state["patient_status"] == "new":
        return {"required_duration": 60}

    elif state["patient_status"] == "returning":
        return {"required_duration": 30}

    return {"required_duration": 0}
def lookup_patient_node(state: AgentState) -> dict:
    """
    Look up the patient in the database and update
    the patient status in the workflow state.
    """
    result = lookup_patient.invoke(
        {
            "first_name": "Sai",
            "last_name": "Sumukh",
            "dob": "2006-05-11"
        }
    )

    return {
        "patient_status": result["status"]
    }


def availability_node(state: AgentState) -> dict:
    """
    Retrieve available doctor slots for the requested
    department and appointment date.
    """

    result = get_doctor_availability.invoke(
        {
            "department": state["department"],
            "appointment_date": state["appointment_date"],
            "duration": state["required_duration"]
        }
    )

    return {
        "available_slots": result
    }

def llm_response(state: AgentState) :
    """
    Simulate an LLM response for testing purposes.
    In a real-world scenario, this function would call an actual LLM API.
    """
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]} 


