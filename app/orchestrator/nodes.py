import json

from app.api.tools.patients import book_appointment, lookup_patient
from app.orchestrator.state import AgentState
from app.api.tools.patients import get_doctor_availability
from app.api.language_chain import llm_with_tools
from langchain_core.messages import AIMessage, ToolMessage


def duration_node(state: AgentState):
    """
    Determine the required duration for the appointment based on the patient's status.
    """
    patient_status = state.get("patient_status")

    if patient_status == "new":
        return {
            "required_duration": 60
        }

    if patient_status == "returning":
        return {
            "required_duration": 30
        }

    return {}


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
    state["patient_status"] = result["status"]
    if result["status"] == "returning":
        state["patient_id"] = result["patient_id"]
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
            "department": state.get("department"),
            "appointment_date": state.get("appointment_date"),
            "duration": state.get("required_duration")
        }
    )

    return {
        "available_slots": result
    }


def llm_response(state: AgentState):
    """
    Simulate an LLM response for testing purposes.
    In a real-world scenario, this function would call an actual LLM API.
    """
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}


def update_workflow_state(state: AgentState):
    """
    Synchronize the workflow state with the latest ToolMessage.

    This node does NOT perform business logic.
    It only copies information returned by tools into AgentState.
    """

    print("\n========== UPDATE WORKFLOW STATE ==========\n")

    last_tool_message = None
    last_ai_message = None

    for message in reversed(state["messages"]):
        if isinstance(message, AIMessage) and message.tool_calls:
            last_ai_message = message
            break
    for message in reversed(state["messages"]):
        if isinstance(message, ToolMessage):
            last_tool_message = message
            break
    if last_tool_message is None:
        print("No ToolMessage found.")
        return {}

    tool_name = last_tool_message.name
    content = last_tool_message.content

    tool_output = (
        json.loads(content)
        if isinstance(content, str)
        else content
    )
    tool_args = {}

    if last_ai_message:
        tool_call = last_ai_message.tool_calls[0]
        tool_args = tool_call["args"]
    print(f"Tool Name   : {tool_name}")
    print(f"Tool Output : {tool_output}")

    if tool_name == "lookup_patient":
        if tool_output.get("status") == "returning":
            return {
                "patient_status": tool_output.get("status"),
                "patient_id": tool_output.get("patient_id"),
            }
        else:
            return {
                "patient_status": tool_output.get("status"),
                "patient_id": None
            }

    elif tool_name == "create_patient":

        return {
            "patient_status": "new",
            "patient_id": tool_output.get("patient_id"),
        }

    elif tool_name == "get_doctor_availability":

        return {
            "appointment_date": tool_args.get("appointment_date"),
            "available_slots": tool_output,
        }
    elif tool_name == "book_appointment":
        from app.email_automation.booking_excel import process_booking
        updated_state = {**state,
                        "booking_confirmed": tool_output.get("success", False),
                        "appointment_id": tool_output.get("appointment_id"),
                        }

        if updated_state["booking_confirmed"]:
         process_booking(updated_state["appointment_id"])

        return updated_state