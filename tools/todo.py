import json
import os

FILE = "data/todo.json"

def load_tasks():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def add_task(task):
    tasks = load_tasks()
    tasks.append({"task": task, "done": False})
    save_tasks(tasks)

def mark_done(task):
    tasks = load_tasks()
    for t in tasks:
        if t["task"].lower().strip() == task.lower().strip():
            t["done"] = True
    save_tasks(tasks)

def get_pending_tasks():
    tasks = load_tasks()
    return [t["task"] for t in tasks if not t["done"]]

def read_tasks():
    return load_tasks()