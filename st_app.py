import streamlit as st
from app.ui.components import render_chat_input, render_header
from app.ui.states import initialize_session
from app.services.agent_services import invoke_agent
from langchain.messages import HumanMessage, AIMessage    
st.set_page_config(
    page_title="Hybrid AI Agent",
    page_icon="🏥",
    layout="wide"
)
initialize_session()
if st.session_state.user_email is None:

    st.title("🏥 Hybrid AI Hospital Assistant")

    st.subheader("Patient Authentication")

    email = st.text_input(
        "Enter your email address"
    )

    if st.button("Continue"):

        if "@" not in email or "." not in email:

            st.error("Please enter a valid email address.")

        else:

            st.session_state.user_email = email

            st.rerun()

    st.stop()
render_header(
    title="🏥 Hybrid AI Hospital Assistant",
    description="Book appointments, check doctor availability and manage patient records."
)
st.subheader("Conversation")

for message in st.session_state.conversation:

    if isinstance(message, HumanMessage):
        role = "user"
    else:
        role = "assistant"

    with st.chat_message(role):

        content = message.content

        if isinstance(content, str):
            st.markdown(content)

        elif isinstance(content, list):
            text = "\n".join(
                block["text"]
                for block in content
                if block.get("type") == "text"
            )

            st.markdown(text)
prompt = render_chat_input()
if prompt:

    st.session_state.conversation.append(
        HumanMessage(content=prompt)
    )
    try:
        with st.spinner("Thinking..."):

            response = invoke_agent(
                st.session_state.conversation
            )
            
            st.session_state.conversation.append(
                response
            )
            
            st.rerun()
    except Exception as e:

         import traceback

         traceback.print_exc()

         st.session_state.conversation.append(
         AIMessage(
            content=str(e)
        )
    )