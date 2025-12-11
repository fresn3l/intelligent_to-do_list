import eel
import json
import os
from datetime import datetime
from typing import List, Dict, Optional

# Initialize Eel with the web folder
eel.init('web')

# Data file paths
DATA_FILE = 'tasks.json'
GOALS_FILE = 'goals.json'
CATEGORIES_FILE = 'categories.json'

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

def load_goals() -> List[Dict]:
    """Load goals from local JSON file"""
    if os.path.exists(GOALS_FILE):
        try:
            with open(GOALS_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def save_goals(goals: List[Dict]):
    """Save goals to local JSON file"""
    with open(GOALS_FILE, 'w') as f:
        json.dump(goals, f, indent=2)

def load_categories() -> List[str]:
    """Load categories from local JSON file"""
    if os.path.exists(CATEGORIES_FILE):
        try:
            with open(CATEGORIES_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def save_categories(categories: List[str]):
    """Save categories to local JSON file"""
    with open(CATEGORIES_FILE, 'w') as f:
        json.dump(categories, f, indent=2)

@eel.expose
def get_tasks():
    """Get all tasks"""
    return load_tasks()

@eel.expose
def add_task(title: str, description: str = "", priority: str = "Next", 
             due_date: str = "", category: str = "", goal_id: Optional[int] = None):
    """Add a new task"""
    tasks = load_tasks()
    new_task = {
        "id": len(tasks) + 1,
        "title": title,
        "description": description,
        "priority": priority,  # Now, Next, Later
        "due_date": due_date,
        "category": category,
        "completed": False,
        "created_at": datetime.now().isoformat(),
        "completed_at": None
    }
    if goal_id is not None:
        new_task["goal_id"] = goal_id
    tasks.append(new_task)
    save_tasks(tasks)
    
    # Add category if it doesn't exist
    if category:
        categories = load_categories()
        if category not in categories:
            categories.append(category)
            save_categories(categories)
    
    return new_task

@eel.expose
def update_task(task_id: int, title: str = None, description: str = None,
                priority: str = None, due_date: str = None, category: str = None,
                goal_id: int = None):
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
                # Add category if it doesn't exist
                if category:
                    categories = load_categories()
                    if category not in categories:
                        categories.append(category)
                        save_categories(categories)
            if goal_id is not None:
                task["goal_id"] = goal_id
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
                completed: bool = None, due_date: str = None, goal_id: int = None):
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
    if goal_id is not None:
        filtered = [task for task in filtered if task.get("goal_id") == goal_id]
    
    return filtered

# Goals management
@eel.expose
def get_goals():
    """Get all goals"""
    return load_goals()

@eel.expose
def add_goal(title: str, description: str = ""):
    """Add a new goal"""
    goals = load_goals()
    new_goal = {
        "id": len(goals) + 1,
        "title": title,
        "description": description,
        "created_at": datetime.now().isoformat()
    }
    goals.append(new_goal)
    save_goals(goals)
    return new_goal

@eel.expose
def update_goal(goal_id: int, title: str = None, description: str = None):
    """Update an existing goal"""
    goals = load_goals()
    for goal in goals:
        if goal["id"] == goal_id:
            if title is not None:
                goal["title"] = title
            if description is not None:
                goal["description"] = description
            save_goals(goals)
            return goal
    return None

@eel.expose
def delete_goal(goal_id: int):
    """Delete a goal and unlink all associated tasks"""
    goals = load_goals()
    goals = [goal for goal in goals if goal["id"] != goal_id]
    save_goals(goals)
    
    # Unlink tasks from deleted goal
    tasks = load_tasks()
    for task in tasks:
        if task.get("goal_id") == goal_id:
            task["goal_id"] = None
    save_tasks(tasks)
    
    return True

# Category management
@eel.expose
def get_categories():
    """Get all categories"""
    return load_categories()

@eel.expose
def add_category(category: str):
    """Add a new category"""
    categories = load_categories()
    if category and category not in categories:
        categories.append(category)
        save_categories(categories)
    return categories

@eel.expose
def delete_category(category: str):
    """Delete a category and remove it from all tasks"""
    categories = load_categories()
    if category in categories:
        categories.remove(category)
        save_categories(categories)
    
    # Remove category from tasks
    tasks = load_tasks()
    for task in tasks:
        if task.get("category") == category:
            task["category"] = ""
    save_tasks(tasks)
    
    return True

@eel.expose
def get_goal_progress(goal_id: int):
    """Get progress statistics for a goal"""
    tasks = load_tasks()
    goal_tasks = [task for task in tasks if task.get("goal_id") == goal_id]
    total = len(goal_tasks)
    completed = len([task for task in goal_tasks if task.get("completed", False)])
    return {
        "total": total,
        "completed": completed,
        "percentage": (completed / total * 100) if total > 0 else 0
    }

# ============================================
# ANALYTICS FUNCTIONS
# ============================================

@eel.expose
def get_analytics():
    """
    Calculate comprehensive analytics for all tasks, categories, goals, and priorities.
    This function aggregates data from all tasks and returns detailed statistics.
    
    Returns:
        dict: Comprehensive analytics including:
            - Overall completion statistics
            - Category-based statistics
            - Priority-based statistics
            - Goal-based statistics
            - Time-based statistics
            - Productivity metrics
    """
    # Load all data from storage
    tasks = load_tasks()
    categories = load_categories()
    goals = load_goals()
    
    # Initialize the analytics dictionary that will hold all our statistics
    analytics = {
        "overall": {},
        "by_category": {},
        "by_priority": {},
        "by_goal": {},
        "time_stats": {},
        "productivity": {}
    }
    
    # ============================================
    # OVERALL STATISTICS
    # ============================================
    # Calculate high-level statistics across all tasks
    
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t.get("completed", False)])
    incomplete_tasks = total_tasks - completed_tasks
    
    # Calculate overall completion percentage
    # Avoid division by zero if no tasks exist
    completion_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    analytics["overall"] = {
        "total": total_tasks,
        "completed": completed_tasks,
        "incomplete": incomplete_tasks,
        "completion_percentage": round(completion_percentage, 2)
    }
    
    # ============================================
    # CATEGORY-BASED STATISTICS
    # ============================================
    # Group tasks by category and calculate stats for each
    
    category_stats = {}
    
    # Process each category
    for category in categories:
        # Filter tasks that belong to this category
        category_tasks = [t for t in tasks if t.get("category") == category]
        cat_total = len(category_tasks)
        cat_completed = len([t for t in category_tasks if t.get("completed", False)])
        cat_incomplete = cat_total - cat_completed
        cat_percentage = (cat_completed / cat_total * 100) if cat_total > 0 else 0
        
        category_stats[category] = {
            "total": cat_total,
            "completed": cat_completed,
            "incomplete": cat_incomplete,
            "completion_percentage": round(cat_percentage, 2)
        }
    
    # Handle uncategorized tasks (tasks without a category)
    uncategorized_tasks = [t for t in tasks if not t.get("category") or t.get("category") == ""]
    if uncategorized_tasks:
        uncat_total = len(uncategorized_tasks)
        uncat_completed = len([t for t in uncategorized_tasks if t.get("completed", False)])
        uncat_incomplete = uncat_total - uncat_completed
        uncat_percentage = (uncat_completed / uncat_total * 100) if uncat_total > 0 else 0
        
        category_stats["Uncategorized"] = {
            "total": uncat_total,
            "completed": uncat_completed,
            "incomplete": uncat_incomplete,
            "completion_percentage": round(uncat_percentage, 2)
        }
    
    analytics["by_category"] = category_stats
    
    # ============================================
    # PRIORITY-BASED STATISTICS
    # ============================================
    # Group tasks by priority level (Now, Next, Later) and calculate stats
    
    priority_stats = {}
    priority_levels = ["Now", "Next", "Later"]
    
    for priority in priority_levels:
        # Filter tasks by this priority level
        priority_tasks = [t for t in tasks if t.get("priority") == priority]
        pri_total = len(priority_tasks)
        pri_completed = len([t for t in priority_tasks if t.get("completed", False)])
        pri_incomplete = pri_total - pri_completed
        pri_percentage = (pri_completed / pri_total * 100) if pri_total > 0 else 0
        
        priority_stats[priority] = {
            "total": pri_total,
            "completed": pri_completed,
            "incomplete": pri_incomplete,
            "completion_percentage": round(pri_percentage, 2)
        }
    
    analytics["by_priority"] = priority_stats
    
    # ============================================
    # GOAL-BASED STATISTICS
    # ============================================
    # Calculate statistics for each goal and tasks linked to goals
    
    goal_stats = {}
    tasks_with_goals = 0
    tasks_without_goals = 0
    
    # Process each goal
    for goal in goals:
        goal_id = goal["id"]
        # Find all tasks linked to this goal
        goal_tasks = [t for t in tasks if t.get("goal_id") == goal_id]
        goal_total = len(goal_tasks)
        goal_completed = len([t for t in goal_tasks if t.get("completed", False)])
        goal_incomplete = goal_total - goal_completed
        goal_percentage = (goal_completed / goal_total * 100) if goal_total > 0 else 0
        
        goal_stats[goal_id] = {
            "goal_name": goal.get("title", "Unknown"),
            "total": goal_total,
            "completed": goal_completed,
            "incomplete": goal_incomplete,
            "completion_percentage": round(goal_percentage, 2)
        }
        
        tasks_with_goals += goal_total
    
    # Count tasks without goals
    tasks_without_goals = len([t for t in tasks if not t.get("goal_id")])
    
    analytics["by_goal"] = {
        "goals": goal_stats,
        "tasks_with_goals": tasks_with_goals,
        "tasks_without_goals": tasks_without_goals,
        "total_goals": len(goals)
    }
    
    # ============================================
    # TIME-BASED STATISTICS
    # ============================================
    # Analyze tasks based on creation dates, completion dates, and due dates
    
    now = datetime.now()
    overdue_count = 0
    due_soon_count = 0  # Due within 7 days
    completed_today = 0
    created_today = 0
    avg_completion_time_days = []
    
    # Process each task for time-based metrics
    for task in tasks:
        # Check if task is overdue (has due date, not completed, past due date)
        if task.get("due_date") and not task.get("completed", False):
            try:
                due_date = datetime.fromisoformat(task["due_date"])
                if due_date < now:
                    overdue_count += 1
                # Check if due within 7 days
                days_until_due = (due_date - now).days
                if 0 <= days_until_due <= 7:
                    due_soon_count += 1
            except (ValueError, TypeError):
                pass  # Skip invalid date formats
        
        # Check if task was completed today
        if task.get("completed_at"):
            try:
                completed_at = datetime.fromisoformat(task["completed_at"])
                if completed_at.date() == now.date():
                    completed_today += 1
                
                # Calculate time to completion if we have both created_at and completed_at
                if task.get("created_at"):
                    try:
                        created_at = datetime.fromisoformat(task["created_at"])
                        time_to_complete = (completed_at - created_at).days
                        if time_to_complete >= 0:  # Only count positive values
                            avg_completion_time_days.append(time_to_complete)
                    except (ValueError, TypeError):
                        pass
            except (ValueError, TypeError):
                pass
        
        # Check if task was created today
        if task.get("created_at"):
            try:
                created_at = datetime.fromisoformat(task["created_at"])
                if created_at.date() == now.date():
                    created_today += 1
            except (ValueError, TypeError):
                pass
    
    # Calculate average completion time
    avg_completion_days = sum(avg_completion_time_days) / len(avg_completion_time_days) if avg_completion_time_days else 0
    
    analytics["time_stats"] = {
        "overdue_count": overdue_count,
        "due_soon_count": due_soon_count,
        "completed_today": completed_today,
        "created_today": created_today,
        "avg_completion_days": round(avg_completion_days, 1)
    }
    
    # ============================================
    # PRODUCTIVITY METRICS
    # ============================================
    # Calculate various productivity indicators
    
    # Find most productive category (highest completion rate with at least 3 tasks)
    most_productive_category = None
    highest_completion_rate = 0
    
    for category, stats in category_stats.items():
        if stats["total"] >= 3 and stats["completion_percentage"] > highest_completion_rate:
            highest_completion_rate = stats["completion_percentage"]
            most_productive_category = category
    
    # Find category with most tasks
    category_with_most_tasks = None
    max_tasks = 0
    for category, stats in category_stats.items():
        if stats["total"] > max_tasks:
            max_tasks = stats["total"]
            category_with_most_tasks = category
    
    # Calculate task distribution (percentage of tasks in each category)
    category_distribution = {}
    for category, stats in category_stats.items():
        if total_tasks > 0:
            category_distribution[category] = round((stats["total"] / total_tasks * 100), 2)
        else:
            category_distribution[category] = 0
    
    analytics["productivity"] = {
        "most_productive_category": most_productive_category,
        "most_productive_completion_rate": round(highest_completion_rate, 2) if most_productive_category else 0,
        "category_with_most_tasks": category_with_most_tasks,
        "max_tasks_in_category": max_tasks,
        "category_distribution": category_distribution
    }
    
    return analytics

if __name__ == '__main__':
    # Start the application
    # Browser options:
    # - 'chrome' (default): Most common, works on all platforms
    # - 'edge': Pre-installed on Windows 10+, must install on macOS/Linux
    # - 'chrome-app': App mode (no browser UI)
    # - None: Use system default browser
    # 
    # Recommendation: Use 'chrome' for best cross-platform compatibility
    # Use 'edge' if targeting Windows users specifically
    eel.start('index.html', size=(900, 700), port=0, mode='chrome-app')

