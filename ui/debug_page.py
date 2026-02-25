import streamlit as st
from memory.short_term import get_messages
from memory.long_term import get_all_memories

def render_debug_page():
    st.title("🧠 Under the Hood")

    st.subheader("Working Memory")
    st.json(get_messages())

    st.subheader("Long-Term Memory")
    st.json(get_all_memories())

    st.subheader("Internal Monologue")
    st.write(st.session_state.get("thought_log", []))