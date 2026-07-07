from typing import TypedDict,Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

    patient_status: str | None
    required_duration: int | None
    booking_confirmed: bool

    department: str | None
    appointment_date: str | None
    available_slots: list[dict]

    patient_id: int | None