from dotenv import load_dotenv
import os
from tools.patients import lookup_patient
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage



load_dotenv()


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

print("LLM created")

llm_with_tools = llm.bind_tools([lookup_patient])

print("Tool bound")
prompt = input("Enter your prompt: ")
response = llm_with_tools.invoke(
    prompt
)

print("Response received")

print("\nTool Calls:")
print(response.tool_calls)

if response.tool_calls:
    tool = response.tool_calls[0]

    name = tool["name"]

    args = tool["args"]
result = lookup_patient.invoke(args)
print("\nTool Result(JSON):\n")
print(result)
print("\ntool result received")