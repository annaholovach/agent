import streamlit as st

def init_memory(system_prompt):
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": system_prompt}
        ]

def get_messages():
    return st.session_state.messages

def add_message(role, content):
    st.session_state.messages.append(
        {"role": role, "content": content}
    )

def clear_short_term():
    st.session_state.messages = []