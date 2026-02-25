import streamlit as st
from agent.agent_loop import run_agent, handle_pending_tasks
from tools.todo import read_tasks, mark_done


def render_agent_page(persona, user_profile):
    st.title(f"{persona['name']} 😜")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "thought_log" not in st.session_state:
        st.session_state.thought_log = []

    if "awaiting_confirmation" not in st.session_state:
        st.session_state.awaiting_confirmation = False
        st.session_state.pending_task = None

    if "proactive_triggered" not in st.session_state:
        st.session_state.proactive_triggered = False


    if not st.session_state.proactive_triggered:
        proactive = handle_pending_tasks()
        if proactive:
            st.session_state.messages.append({
                "role": "assistant",
                "content": proactive["answer"]
            })
            st.session_state.proactive_triggered = True

    user_input = st.text_input("You:", key="input_msg")

    if st.button("Send") and user_input.strip():
        st.session_state.proactive_triggered = False

        if st.session_state.awaiting_confirmation and st.session_state.pending_task:
            if user_input.lower() in ["yes", "yes please", "ok", "do it", "pls do this"]:
                task_to_execute = st.session_state.pending_task

                response = run_agent(
                    [{"role": "user", "content": f"Execute this task: {task_to_execute}"}],
                    user_profile,
                    persona
                )

                if response.get("thought"):
                    st.session_state.thought_log.append(
                        f"Task '{task_to_execute}': {response['thought']}"
                    )

                if response.get("observation"):
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response["observation"]
                    })

                if response.get("answer"):
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response["answer"]
                    })

                mark_done(task_to_execute)

                st.session_state.awaiting_confirmation = False
                st.session_state.pending_task = None

        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        response = run_agent(
            st.session_state.messages,
            user_profile,
            persona
        )

        if response.get("thought"):
            st.session_state.thought_log.append(response["thought"])

        if response.get("answer"):
            st.session_state.messages.append({
                "role": "assistant",
                "content": response["answer"]
            })

        if response.get("observation"):
            st.session_state.messages.append({
                "role": "assistant",
                "content": response["observation"]
            })

    st.subheader("Chat")
    for msg in st.session_state.messages:
        if not msg["content"].strip(): 
            continue
        role = "🧑 You" if msg["role"] == "user" else f"😜 {persona['name']}"
        st.markdown(f"**{role}:** {msg['content']}")

    st.sidebar.header("📝 To-Do Board")
    tasks = read_tasks()
    for t in tasks:
        status = "✅" if t["done"] else "❌"
        st.sidebar.write(f"{status} {t['task']}")


