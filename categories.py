"""
Category Management Module

This module handles all category-related operations:
- Creating and deleting categories
- Managing category lists

All functions decorated with @eel.expose are callable from JavaScript.
"""

import eel
from typing import List

# Import data storage functions
from data_storage import (
    load_categories, save_categories,
    load_tasks, save_tasks
)

# ============================================
# CATEGORY OPERATIONS
# ============================================

@eel.expose
def get_categories():
    """
    Get all categories from storage.
    
    Returns:
        List[str]: All category names in the system
    """
    return load_categories()

@eel.expose
def add_category(category: str):
    """
    Add a new category to the system.
    
    Args:
        category: Category name to add
    
    Returns:
        List[str]: Updated list of all categories
    
    Side Effects:
        - Adds category to categories.json if it doesn't already exist
        - Prevents duplicate categories
    """
    categories = load_categories()
    
    # Only add if category doesn't exist and is not empty
    if category and category not in categories:
        categories.append(category)
        save_categories(categories)
    
    return categories

@eel.expose
def delete_category(category: str):
    """
    Delete a category and remove it from all tasks.
    
    Args:
        category: Category name to delete
    
    Returns:
        bool: True if category was deleted
    
    Side Effects:
        - Removes category from categories.json
        - Removes category from all tasks (sets to empty string)
        - Updates tasks.json with modified tasks
    """
    categories = load_categories()
    
    # Remove category from list if it exists
    if category in categories:
        categories.remove(category)
        save_categories(categories)
    
    # Remove category from all tasks
    # This prevents orphaned category references
    tasks = load_tasks()
    for task in tasks:
        if task.get("category") == category:
            task["category"] = ""
    save_tasks(tasks)
    
    return True

