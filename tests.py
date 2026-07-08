from app.orchestrator.graph import graph
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

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
       print("\n========== FINAL AGENT STATE ==========\n")

       for key, value in state.items():
        print(f"{key}:")
        print(value)
        print()

       break

    state["messages"].append(
        HumanMessage(content=user_input)
    )

    state = graph.invoke(state)
    print("\n========== AGENT STATE ==========")
    print(f"Patient Status      : {state['patient_status']}")
    print(f"Required Duration   : {state['required_duration']}")
    print(f"Booking Confirmed   : {state['booking_confirmed']}")
    print("=================================\n")
    last_message = state["messages"][-1]
    print(last_message)
    print(type(last_message))
    print(last_message.__dict__)
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
