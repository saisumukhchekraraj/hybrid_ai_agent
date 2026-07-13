print("Importing graph...")

from app.orchestrator.graph import graph

print("Graph imported.")
def invoke_agent(messages):
    """
    Invokes the agent with the provided messages and returns the response.
    """
    response = graph.invoke({"messages": messages})
    return response["messages"][-1]