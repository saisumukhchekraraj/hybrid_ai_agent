from app.orchestrator.graph import graph
from langchain_core.messages import HumanMessage, AIMessage

state = {
    "messages": [],
    "patient_status": None,
    "required_duration": None,
    "booking_confirmed": False,
    "department": None,
    "appointment_date": None,
    "available_slots": [],
}

print("Hybrid AI Agent")
print("Type 'exit' to quit.\n")

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    state["messages"].append(
        HumanMessage(content=user_input)
    )

    state = graph.invoke(state)

    last_message = state["messages"][-1]

    if isinstance(last_message, AIMessage):

        # Gemini responses can be plain strings or structured content.
        if isinstance(last_message.content, str):
            print(f"\nAssistant: {last_message.content}\n")
        elif isinstance(last_message.content, list):
            text = ""
            for block in last_message.content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text += block.get("text", "")
            print(f"\nAssistant: {text}\n")