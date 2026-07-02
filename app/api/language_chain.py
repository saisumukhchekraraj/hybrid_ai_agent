import json

from dotenv import load_dotenv
import os
from tools.patients import (lookup_patient, create_patient, get_doctor_availability, book_appointment)
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_core.messages import ToolMessage
from langchain_core.messages import AIMessage


load_dotenv()


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

print("LLM created")

TOOLS = {
    "lookup_patient": lookup_patient,
    "create_patient": create_patient,
    "get_doctor_availability": get_doctor_availability,
    "book_appointment": book_appointment,
}

llm_with_tools = llm.bind_tools(list(TOOLS.values()))
print("Tool bound")
prompt = input("Enter your prompt: ")
messages = [HumanMessage(content=prompt)]




MAX_ITERATIONS = 10



for iteration in range(MAX_ITERATIONS):



    print(f"\n========== Iteration {iteration+1} ==========\n")



    response = llm_with_tools.invoke(messages)



    # Save Gemini's response

    messages.append(response)



    # Finished

    if not response.tool_calls:

        print("\nFinal Response:\n")

        print(response.content)

        break



    # Execute every tool Gemini requested

    for tool_call in response.tool_calls:



        tool_name = tool_call["name"]

        tool_args = tool_call["args"]



        print(f"\nTool Selected : {tool_name}")

        print(tool_args)



        result = TOOLS[tool_name].invoke(tool_args)



        print("\nTool Result:")

        print(result)



        # Give the result back to Gemini

        messages.append(

            ToolMessage(

                content=json.dumps(result),

                tool_call_id=tool_call["id"],

            )

        )



else:

    print("\nMaximum iterations reached.")
