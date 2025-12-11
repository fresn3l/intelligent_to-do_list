"""
Todo/Task Management Module

This module handles all task-related operations:
- Creating, reading, updating, deleting tasks
- Searching and filtering tasks
- Task completion management

All functions decorated with @eel.expose are callable from JavaScript.
"""

import eel
from datetime import datetime
from typing import List, Dict, Optional

# Import data storage functions
from data_storage import (
    load_tasks, save_tasks
)

# ============================================
# TASK CRUD OPERATIONS
# ============================================

@eel.expose
def get_tasks():
    """
    Get all tasks from storage.
    
    Returns:
        List[Dict]: All tasks in the system
    """
    return load_tasks()

@eel.expose
def add_task(title: str, description: str = "", priority: str = "Next", 
             due_date: str = "", goal_id: Optional[int] = None):
    """
    Add a new task to the system.
    
    Args:
        title: Task title (required)
        description: Task description (optional)
        priority: Priority level - "Now", "Next", or "Later" (default: "Next")
        due_date: Due date in ISO format (optional)
        goal_id: ID of linked goal (required)
    
    Returns:
        Dict: The newly created task dictionary
    
    Side Effects:
        - Saves task to tasks.json
    """
    tasks = load_tasks()
    
    # Create new task dictionary with all properties
    new_task = {
        "id": len(tasks) + 1,
        "title": title,
        "description": description,
        "priority": priority,  # Now, Next, Later
        "due_date": due_date,
        "completed": False,
        "created_at": datetime.now().isoformat(),
        "completed_at": None
    }
    
    # Add goal_id (required)
    if goal_id is not None:
        new_task["goal_id"] = goal_id
    
    # Add task to list and save
    tasks.append(new_task)
    save_tasks(tasks)
    
    return new_task

@eel.expose
def update_task(task_id: int, title: str = None, description: str = None,
                priority: str = None, due_date: str = None,
                goal_id: int = None):
    """
    Update an existing task.
    
    Args:
        task_id: ID of task to update
        title: New title (optional - only updates if provided)
        description: New description (optional)
        priority: New priority (optional)
        due_date: New due date (optional)
        goal_id: New goal ID (optional)
    
    Returns:
        Dict: Updated task dictionary, or None if task not found
    
    Side Effects:
        - Updates task in tasks.json
    """
    tasks = load_tasks()
    
    # Find task by ID
    for task in tasks:
        if task["id"] == task_id:
            # Update only provided fields (None means "don't change")
            if title is not None:
                task["title"] = title
            if description is not None:
                task["description"] = description
            if priority is not None:
                task["priority"] = priority
            if due_date is not None:
                task["due_date"] = due_date
            if goal_id is not None:
                task["goal_id"] = goal_id
            
            # Save updated tasks
            save_tasks(tasks)
            return task
    
    # Task not found
    return None

@eel.expose
def toggle_task(task_id: int):
    """
    Toggle task completion status.
    
    Args:
        task_id: ID of task to toggle
    
    Returns:
        Dict: Updated task dictionary, or None if task not found
    
    Side Effects:
        - Updates task.completed in tasks.json
        - Sets/clears completed_at timestamp
    """
    tasks = load_tasks()
    
    # Find task by ID
    for task in tasks:
        if task["id"] == task_id:
            # Toggle completion status
            task["completed"] = not task["completed"]
            
            # Update completion timestamp
            if task["completed"]:
                task["completed_at"] = datetime.now().isoformat()
            else:
                task["completed_at"] = None
            
            # Save updated tasks
            save_tasks(tasks)
            return task
    
    # Task not found
    return None

@eel.expose
def delete_task(task_id: int):
    """
    Delete a task from the system.
    
    Args:
        task_id: ID of task to delete
    
    Returns:
        bool: True if task was deleted, False otherwise
    
    Side Effects:
        - Removes task from tasks.json
    """
    tasks = load_tasks()
    
    # Filter out the task with matching ID
    original_count = len(tasks)
    tasks = [task for task in tasks if task["id"] != task_id]
    
    # Only save if a task was actually removed
    if len(tasks) < original_count:
        save_tasks(tasks)
        return True
    
    return False

# ============================================
# TASK SEARCH AND FILTER
# ============================================

@eel.expose
def search_tasks(query: str):
    """
    Search tasks by title or description.
    
    Args:
        query: Search query string (case-insensitive)
    
    Returns:
        List[Dict]: Tasks matching the search query
    
    Search Logic:
        - Searches in task title
        - Searches in task description
        - Case-insensitive matching
    """
    tasks = load_tasks()
    query_lower = query.lower()
    
    # Filter tasks that match search query
    filtered = [
        task for task in tasks
        if query_lower in task["title"].lower() or
           query_lower in task.get("description", "").lower()
    ]
    
    return filtered

@eel.expose
def filter_tasks(priority: str = None, 
                completed: bool = None, due_date: str = None, goal_id: int = None):
    """
    Filter tasks by various criteria.
    
    Args:
        priority: Filter by priority level (optional)
        completed: Filter by completion status (optional)
        due_date: Filter by due date (optional)
        goal_id: Filter by linked goal ID (optional)
    
    Returns:
        List[Dict]: Tasks matching all provided filters
    
    Filter Logic:
        - All filters are ANDed together (must match all)
        - None values mean "don't filter by this criteria"
    """
    tasks = load_tasks()
    filtered = tasks
    
    # Apply each filter if provided
    if priority:
        filtered = [task for task in filtered if task["priority"] == priority]
    if completed is not None:
        filtered = [task for task in filtered if task["completed"] == completed]
    if due_date:
        filtered = [task for task in filtered if task.get("due_date") == due_date]
    if goal_id is not None:
        filtered = [task for task in filtered if task.get("goal_id") == goal_id]
    
    return filtered

