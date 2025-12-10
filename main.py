import eel
import json
import os
from datetime import datetime
from typing import List, Dict, Optional

# Initialize Eel with the web folder
eel.init('web')

# Data file path
DATA_FILE = 'tasks.json'

def load_tasks() -> List[Dict]:
    """Load tasks from local JSON file"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def save_tasks(tasks: List[Dict]):
    """Save tasks to local JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

@eel.expose
def get_tasks():
    """Get all tasks"""
    return load_tasks()

@eel.expose
def add_task(title: str, description: str = "", priority: str = "medium", 
             due_date: str = "", category: str = ""):
    """Add a new task"""
    tasks = load_tasks()
    new_task = {
        "id": len(tasks) + 1,
        "title": title,
        "description": description,
        "priority": priority,  # low, medium, high
        "due_date": due_date,
        "category": category,
        "completed": False,
        "created_at": datetime.now().isoformat(),
        "completed_at": None
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return new_task

@eel.expose
def update_task(task_id: int, title: str = None, description: str = None,
                priority: str = None, due_date: str = None, category: str = None):
    """Update an existing task"""
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            if title is not None:
                task["title"] = title
            if description is not None:
                task["description"] = description
            if priority is not None:
                task["priority"] = priority
            if due_date is not None:
                task["due_date"] = due_date
            if category is not None:
                task["category"] = category
            save_tasks(tasks)
            return task
    return None

@eel.expose
def toggle_task(task_id: int):
    """Toggle task completion status"""
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            if task["completed"]:
                task["completed_at"] = datetime.now().isoformat()
            else:
                task["completed_at"] = None
            save_tasks(tasks)
            return task
    return None

@eel.expose
def delete_task(task_id: int):
    """Delete a task"""
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)
    return True

@eel.expose
def search_tasks(query: str):
    """Search tasks by title, description, or category"""
    tasks = load_tasks()
    query_lower = query.lower()
    filtered = [
        task for task in tasks
        if query_lower in task["title"].lower() or
           query_lower in task.get("description", "").lower() or
           query_lower in task.get("category", "").lower()
    ]
    return filtered

@eel.expose
def filter_tasks(priority: str = None, category: str = None, 
                completed: bool = None, due_date: str = None):
    """Filter tasks by various criteria"""
    tasks = load_tasks()
    filtered = tasks
    
    if priority:
        filtered = [task for task in filtered if task["priority"] == priority]
    if category:
        filtered = [task for task in filtered if task.get("category") == category]
    if completed is not None:
        filtered = [task for task in filtered if task["completed"] == completed]
    if due_date:
        filtered = [task for task in filtered if task.get("due_date") == due_date]
    
    return filtered

if __name__ == '__main__':
    # Start the application
    eel.start('index.html', size=(900, 700), port=0)

