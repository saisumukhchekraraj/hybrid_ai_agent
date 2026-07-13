import streamlit as st
from langchain.messages import HumanMessage, AIMessage
def initialize_session():
    if "conversation" not in st.session_state:
        st.session_state.conversation = []
        st.session_state.conversation = [
            AIMessage(content="Hello! I am your Hybrid AI Hospital Assistant.\n\nHow can I help you today?")
        ]