from langchain_core.messages import HumanMessage
from app.services.agent_services import invoke_agent

response = invoke_agent(
    [
        HumanMessage(
            content="Hello"
        )
    ]
)

print(response)