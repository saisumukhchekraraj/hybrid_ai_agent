from dotenv import load_dotenv
import os
from tools.patients import lookup_patient
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

print("1. Starting...")

load_dotenv()

print("2. Environment loaded")

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

print("3. LLM created")

llm_with_tools = llm.bind_tools([lookup_patient])

print("4. Tool bound")
response1 = llm.invoke("Hello")

print(response1.content) 
print("response 1 recieved")
response2 = llm_with_tools.invoke(
    "What is 2 + 2?"
) 
print(response2)
print("response 2 recieved")
response = llm_with_tools.invoke(
    "My name is Sai Sumukh and my DOB is 2006-05-11."
)

print("5. Response received")

print(response)
