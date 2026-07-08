from langgraph.graph import StateGraph, START, END
from langchain_core.messages import AIMessage
from app.orchestrator.state import AgentState
from app.orchestrator.nodes import availability_node, duration_node, lookup_patient_node , llm_response , update_workflow_state
from app.api.tools.patients import create_patient, lookup_patient, get_doctor_availability, book_appointment
from langgraph.prebuilt import ToolNode
tool_node = ToolNode([
    lookup_patient,
    get_doctor_availability,
    book_appointment,
    create_patient
])

def route_after_llm(state):

    last_message = state["messages"][-1]

    if (
        isinstance(last_message, AIMessage)
        and last_message.tool_calls
    ):
        return "tools"

    return "__end__"
builder = StateGraph(AgentState)
builder.add_node("update_state", update_workflow_state)
builder.add_node("duration", duration_node)
builder.add_node("llm", llm_response)
builder.add_node("tools", tool_node)

builder.set_entry_point("llm")

builder.add_conditional_edges(
    "llm",
    route_after_llm,
    {
        "tools": "tools",
        "__end__": END,
    }
)

builder.add_edge("tools", "update_state")
builder.add_edge("update_state", "duration")
builder.add_edge("duration", "llm")

graph = builder.compile()



