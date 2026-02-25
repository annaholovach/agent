import streamlit as st
from ui.agent_page import render_agent_page
from ui.debug_page import render_debug_page
from memory.short_term import init_memory

st.set_page_config(layout="wide")

st.sidebar.header("⚙️ Configuration")

user_profile = {
    "name": st.sidebar.text_input("User Name", "Anna"),
    "info": st.sidebar.text_area("User Info", "AI enthusiast")
}

persona = {
    "name": st.sidebar.text_input("Agent Name", "Nova"),
    "role": st.sidebar.text_input("Agent Role", "Personal Assistant"),
    "instructions": st.sidebar.text_area(
        "System Instructions",
        "Be concise and proactive."
    )
}

init_memory("")

page = st.sidebar.radio("Navigation", ["Agent", "Under the Hood"])

if page == "Agent":
    render_agent_page(persona, user_profile)
else:
    render_debug_page()