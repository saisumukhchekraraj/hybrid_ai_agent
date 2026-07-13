from dotenv import load_dotenv
import os

from langchain_google_genai import ChatGoogleGenerativeAI

from app.api.tools.patients import (
    lookup_patient,
    create_patient,
    get_doctor_availability,
    book_appointment,
)

load_dotenv()
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)

llm_with_tools = llm.bind_tools(
    [
        lookup_patient,
        create_patient,
        get_doctor_availability,
        book_appointment,
    ]
)