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