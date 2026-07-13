import streamlit as st
def render_header(title: str, description: str):
    """
    Displays the application title and description.
    """

    st.title(title)
    st.write(
        description
    )

    st.divider()
    
def render_chat_input():

    return st.chat_input(
        "Type your message..."
    )
