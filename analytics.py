"""
Analytics Module

This module calculates comprehensive analytics and statistics:
- Overall completion statistics
- Category-based analytics
- Priority-based analytics
- Goal-based analytics
- Time-based analytics
- Productivity metrics

All functions decorated with @eel.expose are callable from JavaScript.
"""

import eel
from datetime import datetime
from typing import List, Dict

# Import data storage functions
from data_storage import load_tasks, load_goals

# ============================================
# ANALYTICS FUNCTIONS
# ============================================

@eel.expose
def get_analytics():
    """
    Calculate comprehensive analytics for all tasks, categories, goals, and priorities.
    
    This function aggregates data from all tasks and returns detailed statistics
    that can be used for data visualization and insights.
    
    Returns:
        dict: Comprehensive analytics dictionary with the following structure:
            {
                "overall": {
                    "total": int,
                    "completed": int,
                    "incomplete": int,
                    "completion_percentage": float
                },
                "by_category": {
                    "CategoryName": {
                        "total": int,
                        "completed": int,
                        "incomplete": int,
                        "completion_percentage": float
                    },
                    ...
                },
                "by_priority": {
                    "Now": {...},
                    "Next": {...},
                    "Later": {...}
                },
                "by_goal": {
                    "goals": {...},
                    "tasks_with_goals": int,
                    "tasks_without_goals": int,
                    "total_goals": int
                },
                "time_stats": {
                    "overdue_count": int,
                    "due_soon_count": int,
                    "completed_today": int,
                    "created_today": int,
                    "avg_completion_days": float
                },
                "productivity": {
                    "most_productive_category": str,
                    "most_productive_completion_rate": float,
                    "category_with_most_tasks": str,
                    "max_tasks_in_category": int,
                    "category_distribution": {...}
                }
            }
    
    Algorithm Overview:
        1. Load all data (tasks, categories, goals)
        2. Calculate overall statistics
        3. Group and calculate category statistics
        4. Group and calculate priority statistics
        5. Group and calculate goal statistics
        6. Calculate time-based metrics
        7. Calculate productivity insights
        8. Return comprehensive analytics dictionary
    """
    # ============================================
    # STEP 1: LOAD ALL DATA
    # ============================================
    # Load all data from storage files
    tasks = load_tasks()
    goals = load_goals()
    
    # Initialize the analytics dictionary structure
    # This will hold all calculated statistics
    analytics = {
        "overall": {},
        "by_goal": {},
        "by_priority": {},
        "time_stats": {},
        "productivity": {}
    }
    
    # ============================================
    # STEP 2: OVERALL STATISTICS
    # ============================================
    # Calculate high-level statistics across all tasks
    # These give a quick overview of task completion
    
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
    # STEP 3: PRIORITY-BASED STATISTICS
    # ============================================
    # Group tasks by priority level (Now, Next, Later) and calculate stats
    # This shows how well you're handling high-priority tasks
    
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
    # STEP 4: GOAL-BASED STATISTICS
    # ============================================
    # Calculate statistics for each goal and tasks linked to goals
    # This tracks progress toward your goals
    
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
    # STEP 5: TIME-BASED STATISTICS
    # ============================================
    # Analyze tasks based on creation dates, completion dates, and due dates
    # This provides insights into time management and productivity patterns
    
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
    # Sum all completion times and divide by count
    avg_completion_days = sum(avg_completion_time_days) / len(avg_completion_time_days) if avg_completion_time_days else 0
    
    analytics["time_stats"] = {
        "overdue_count": overdue_count,
        "due_soon_count": due_soon_count,
        "completed_today": completed_today,
        "created_today": created_today,
        "avg_completion_days": round(avg_completion_days, 1)
    }
    
    # ============================================
    # STEP 6: PRODUCTIVITY METRICS
    # ============================================
    # Calculate various productivity indicators
    # These help identify patterns and areas for improvement
    
    # Find most productive category (highest completion rate with at least 3 tasks)
    # This identifies where you're most effective
    most_productive_category = None
    highest_completion_rate = 0
    
    for category, stats in category_stats.items():
        if stats["total"] >= 3 and stats["completion_percentage"] > highest_completion_rate:
            highest_completion_rate = stats["completion_percentage"]
            most_productive_category = category
    
    # Find category with most tasks
    # This shows where you focus most of your effort
    category_with_most_tasks = None
    max_tasks = 0
    for category, stats in category_stats.items():
        if stats["total"] > max_tasks:
            max_tasks = stats["total"]
            category_with_most_tasks = category
    
    # Calculate task distribution (percentage of tasks in each category)
    # This shows how tasks are distributed across categories
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
    
    # ============================================
    # STEP 8: RETURN ANALYTICS
    # ============================================
    # Return the complete analytics dictionary
    # This will be sent to JavaScript for display
    return analytics

