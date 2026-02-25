import ollama
import json
from tools.search import search_tool
from tools.todo import add_task, read_tasks, mark_done
from memory.long_term import query_memory, save_memory
from prompts.persona import build_system_prompt

client = ollama.Client(host="http://localhost:11434")


def execute_tool(action, action_input):
    if action == "search" and action_input:
        return search_tool(action_input)

    elif action == "todo_add" and action_input:
        add_task(action_input)
        return "Task added."

    elif action == "todo_read":
        tasks = read_tasks()
        if not tasks:
            return "No tasks."
        return "\n".join(
            f"{'(done)' if t['done'] else '(pending)'} {t['task']}"
            for t in tasks
        )

    elif action == "todo_done" and action_input:
        mark_done(action_input)
        return "Task marked done."

    elif action == "save_memory" and action_input:
        save_memory(action_input)
        return "Memory saved."

    return ""


def run_agent(messages, user_profile, persona):
    user_input = messages[-1]["content"]

    memory_chunks = query_memory(user_input)
    memory_context = "\n".join(memory_chunks) if memory_chunks else ""

    system_prompt = build_system_prompt(user_profile, persona, memory_context)

    response = client.chat(
        model="llama3",
        messages=[
            {"role": "system", "content": system_prompt},
            *messages
        ],
        options={"temperature": 0}
    )

    raw = response["message"]["content"]

    try:
        data = json.loads(raw)
    except:
        return {
            "answer": raw,
            "thought": "",
            "observation": ""
        }

    thought = data.get("thought", "")
    action = data.get("action", "none")
    action_input = data.get("action_input", "")
    final_answer = data.get("final_answer", "")

    observation = ""

    if action != "none":
        observation = execute_tool(action, action_input)

    return {
        "answer": final_answer,
        "thought": thought,
        "observation": observation
    }


def handle_pending_tasks():
    tasks = read_tasks()

    for task in tasks:
        if not task["done"]:
            return {
                "answer": f"I see we still need to '{task['task']}'. Shall I do it now?"
            }

    return None

