# Code Walkthrough: Line-by-Line Explanation

This document provides a detailed, line-by-line explanation of the codebase. Use it as a reference while reading the code.

## Table of Contents

- [main.py - Complete Walkthrough](#mainpy---complete-walkthrough)
- [app.js - Complete Walkthrough](#appjs---complete-walkthrough)
- [index.html - Complete Walkthrough](#indexhtml---complete-walkthrough)
- [style.css - Key Concepts](#stylecss---key-concepts)

---

## main.py - Complete Walkthrough

### Lines 1-5: Imports

```python
import eel
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
```

**Line 1**: `eel` - The desktop app framework
- Provides `@eel.expose` decorator and `eel.start()` function
- Creates bridge between Python and JavaScript

**Line 2**: `json` - JSON file handling
- `json.load()`: Read JSON from file → Python data
- `json.dump()`: Write Python data → JSON file

**Line 3**: `os` - Operating system interface
- `os.path.exists()`: Check if file exists
- Used to avoid errors when `tasks.json` doesn't exist yet

**Line 4**: `datetime` - Date and time handling
- `datetime.now()`: Current date/time
- `.isoformat()`: Convert to string like "2024-01-15T10:30:00"

**Line 5**: `typing` - Type hints
- `List[Dict]`: Type hint meaning "list of dictionaries"
- Makes code self-documenting and helps catch errors

### Lines 7-8: Eel Initialization

```python
# Initialize Eel with the web folder
eel.init('web')
```

**What it does**: Tells Eel where to find HTML/CSS/JavaScript files
- `'web'` is the folder name
- Eel will serve files from `web/` directory
- Must be called before any `@eel.expose` decorators

### Lines 10-11: Constants

```python
# Data file path
DATA_FILE = 'tasks.json'
```

**Why a constant?**
- If we need to change the filename, only change it here
- Prevents typos (using `'tasks.json'` in multiple places)
- Makes code more maintainable

### Lines 13-21: load_tasks() Function

```python
def load_tasks() -> List[Dict]:
    """Load tasks from local JSON file"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []
```

**Line 13**: Function definition with return type hint
- `-> List[Dict]`: This function returns a list of dictionaries

**Line 15**: Check if file exists
- Prevents `FileNotFoundError` on first run
- Returns empty list if file doesn't exist

**Line 16**: Try block - attempt to read file
- If anything goes wrong, `except` block handles it

**Line 17**: Context manager for file reading
- `with open(...)`: Automatically closes file when done
- `'r'`: Read mode (text mode)
- `as f`: File object named `f`

**Line 18**: Parse JSON into Python data
- `json.load(f)`: Reads file and converts JSON → Python
- Returns list of task dictionaries

**Line 19**: Exception handling
- `json.JSONDecodeError`: File exists but isn't valid JSON
- `IOError`: File exists but can't be read (permissions, etc.)
- Returns empty list instead of crashing

**Line 21**: Return empty list if file doesn't exist

### Lines 23-26: save_tasks() Function

```python
def save_tasks(tasks: List[Dict]):
    """Save tasks to local JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)
```

**Line 23**: Function takes list of task dictionaries

**Line 25**: Context manager for file writing
- `'w'`: Write mode (overwrites existing file)
- `'a'` would append, `'r'` would read

**Line 26**: Convert Python data to JSON
- `json.dump()`: Writes Python data as JSON text
- `indent=2`: Pretty printing (2 spaces per level)
- Makes file human-readable for debugging

### Lines 28-31: get_tasks() - Exposed Function

```python
@eel.expose
def get_tasks():
    """Get all tasks"""
    return load_tasks()
```

**Line 28**: `@eel.expose` decorator
- Makes function callable from JavaScript
- Without this, JavaScript can't access the function

**Line 30**: Simple wrapper function
- Calls `load_tasks()` and returns result
- JavaScript calls this: `await eel.get_tasks()()`

### Lines 33-51: add_task() - Exposed Function

```python
@eel.expose
def add_task(title: str, description: str = "", priority: str = "medium", 
             due_date: str = "", category: str = ""):
    """Add a new task"""
    tasks = load_tasks()
    new_task = {
        "id": len(tasks) + 1,
        "title": title,
        "description": description,
        "priority": priority,  # now, next, later
        "due_date": due_date,
        "category": category,
        "completed": False,
        "created_at": datetime.now().isoformat(),
        "completed_at": None
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return new_task
```

**Line 34**: Function signature with default parameters
- `description: str = ""`: Default empty string if not provided
- Makes function flexible - some fields optional

**Line 37**: Load existing tasks
- Need current list to generate new ID

**Lines 38-48**: Create task dictionary
- **Line 39**: `"id": len(tasks) + 1` - Simple ID generation
  - First task gets ID 1, second gets 2, etc.
  - **Note**: This can create duplicate IDs if tasks are deleted
  - Production apps use UUIDs or database auto-increment
- **Line 46**: `"completed": False` - New tasks start incomplete
- **Line 47**: `datetime.now().isoformat()` - Timestamp string
- **Line 48**: `"completed_at": None` - Will be set when completed

**Line 49**: Add to list
- `append()` adds item to end of list

**Line 50**: Save to file
- Persists new task to disk

**Line 51**: Return the new task
- JavaScript can use this to update UI immediately

### Lines 53-72: update_task() - Exposed Function

```python
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
```

**Line 54**: All parameters default to `None`
- Allows partial updates (only change what's provided)
- `None` means "not provided", different from `""` (empty string)

**Line 57**: Loop through all tasks
- Linear search: checks each task until match found
- For small lists (< 1000), this is fine
- For large lists, use dictionary: `tasks_by_id[task_id]`

**Line 58**: Check if IDs match
- `==` compares values
- `is` compares identity (use `is None`, not `== None`)

**Lines 59-68**: Conditional updates
- Only updates fields that were provided (not `None`)
- Allows changing just title, keeping description unchanged

**Line 69**: Save changes to file
- Must save after modifying

**Line 70**: Return updated task
- JavaScript can use this to update UI

**Line 71**: Return `None` if task not found
- Indicates failure to JavaScript

### Lines 74-87: toggle_task() - Exposed Function

```python
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
```

**Line 79**: Boolean toggle
- `not task["completed"]` flips True ↔ False
- Elegant way to toggle

**Lines 80-84**: Conditional timestamp
- If completing: record current time
- If uncompleting: clear timestamp
- Tracks when tasks were finished

### Lines 89-95: delete_task() - Exposed Function

```python
@eel.expose
def delete_task(task_id: int):
    """Delete a task"""
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)
    return True
```

**Line 93**: List comprehension
- Creates new list with all tasks EXCEPT the one to delete
- Equivalent to:
  ```python
  filtered = []
  for task in tasks:
      if task["id"] != task_id:
          filtered.append(task)
  tasks = filtered
  ```
- More concise and Pythonic

### Lines 97-108: search_tasks() - Exposed Function

```python
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
```

**Line 101**: Case-insensitive search
- Convert both query and text to lowercase
- "Python" matches "python"

**Lines 102-107**: List comprehension with multiple conditions
- Searches title, description, AND category
- `or` means match if ANY field contains query
- `.get("description", "")`: Safe access, returns `""` if key missing

### Lines 110-126: filter_tasks() - Exposed Function

```python
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
```

**Line 115**: Start with all tasks
- Each filter narrows down results

**Lines 117-124**: Chained filters
- Each `if` statement applies another filter
- Filters are ANDed together (must match all)
- `completed is not None`: Special check because `False` is falsy
  - `if completed:` would fail when `completed=False`
  - `is not None` checks if parameter was provided

### Lines 128-130: Application Entry Point

```python
if __name__ == '__main__':
    # Start the application
    eel.start('index.html', size=(900, 700), port=0)
```

**Line 128**: Python idiom
- `__name__` is `'__main__'` when file is run directly
- Allows file to be both module and script
- Code only runs if executed directly (not imported)

**Line 130**: Start Eel application
- Opens desktop window
- Loads `index.html`
- `size=(900, 700)`: Window dimensions (width, height)
- `port=0`: Auto-selects available port

---

## app.js - Complete Walkthrough

### Lines 1-7: Global State Variables

```javascript
let tasks = [];
let showCompleted = false;
let currentFilter = {
    priority: '',
    category: '',
    search: ''
};
```

**Line 1**: `tasks` - Array holding all tasks
- Loaded from backend on startup
- Updated when tasks are added/modified/deleted

**Line 2**: `showCompleted` - Boolean flag
- Controls whether completed tasks are visible
- Toggled by "Show Completed" button

**Line 3-6**: `currentFilter` - Object storing filter state
- Tracks active filters (priority, category, search)
- Used when rendering tasks

### Lines 9-13: init() Function

```javascript
async function init() {
    await loadTasks();
    setupEventListeners();
}
```

**Line 9**: `async function` - Can use `await` keyword
- Needed because `loadTasks()` is asynchronous

**Line 10**: Load tasks from backend
- `await`: Waits for `loadTasks()` to complete
- Tasks are stored in global `tasks` variable

**Line 11**: Set up event listeners
- Attaches handlers to buttons, forms, inputs
- Must be done after page loads

### Lines 15-24: loadTasks() Function

```javascript
async function loadTasks() {
    try {
        tasks = await eel.get_tasks()();
        renderTasks();
        updateCategoryFilter();
    } catch (error) {
        console.error('Error loading tasks:', error);
    }
}
```

**Line 16**: Try block - attempt to load tasks
- If it fails, catch block handles error

**Line 17**: Call Python function via Eel
- `eel.get_tasks()`: Returns a promise
- `()`: Calls the function (no arguments)
- `await`: Waits for Python to respond
- Result stored in `tasks` variable

**Line 18**: Render tasks in UI
- Updates the display with current tasks

**Line 19**: Update category filter dropdown
- Adds any new categories to the filter list

**Lines 20-22**: Error handling
- Logs error to console
- App continues running (doesn't crash)

### Lines 26-38: setupEventListeners() Function

```javascript
function setupEventListeners() {
    // Form submission
    document.getElementById('taskForm').addEventListener('submit', handleAddTask);
    
    // Search
    document.getElementById('searchInput').addEventListener('input', handleSearch);
    
    // Filters
    document.getElementById('filterPriority').addEventListener('change', handleFilterChange);
    document.getElementById('filterCategory').addEventListener('change', handleFilterChange);
    document.getElementById('showCompleted').addEventListener('click', toggleCompleted);
}
```

**Line 29**: Form submit listener
- `'submit'`: Event fires when form is submitted
- `handleAddTask`: Function to call

**Line 32**: Search input listener
- `'input'`: Fires on every keystroke
- Real-time search as user types

**Lines 35-36**: Filter change listeners
- `'change'`: Fires when dropdown selection changes
- Updates filter and re-renders

**Line 37**: Button click listener
- `'click'`: Fires when button is clicked
- Toggles completed tasks visibility

### Lines 40-60: handleAddTask() Function

```javascript
async function handleAddTask(e) {
    e.preventDefault();
    
    const title = document.getElementById('taskTitle').value.trim();
    const description = document.getElementById('taskDescription').value.trim();
    const priority = document.getElementById('taskPriority').value;
    const dueDate = document.getElementById('taskDueDate').value;
    const category = document.getElementById('taskCategory').value.trim();
    
    if (!title) return;
    
    try {
        await eel.add_task(title, description, priority, dueDate, category)();
        document.getElementById('taskForm').reset();
        await loadTasks();
    } catch (error) {
        console.error('Error adding task:', error);
        alert('Failed to add task. Please try again.');
    }
}
```

**Line 41**: `e.preventDefault()`
- Stops form's default submit behavior
- Without this, page would refresh (losing state)

**Lines 44-48**: Get form values
- `.value`: Gets input's current value
- `.trim()`: Removes leading/trailing whitespace
- `const`: Variable can't be reassigned

**Line 50**: Validation
- Early return if title is empty
- Prevents unnecessary API call

**Line 53**: Call Python function
- Sends form data to backend
- `await`: Waits for response

**Line 54**: Reset form
- Clears all inputs
- Ready for next task

**Line 55**: Reload tasks
- Refreshes display to show new task

**Lines 56-59**: Error handling
- Shows user-friendly alert
- Logs error for debugging

### Lines 62-66: handleSearch() Function

```javascript
function handleSearch(e) {
    currentFilter.search = e.target.value.toLowerCase();
    renderTasks();
}
```

**Line 63**: Update filter state
- `e.target`: The input element that fired event
- `.value`: Current text in input
- `.toLowerCase()`: Case-insensitive search
- Stores in `currentFilter.search`

**Line 64**: Re-render tasks
- Applies new search filter
- Updates display immediately

### Lines 68-73: handleFilterChange() Function

```javascript
function handleFilterChange() {
    currentFilter.priority = document.getElementById('filterPriority').value;
    currentFilter.category = document.getElementById('filterCategory').value;
    renderTasks();
}
```

**Lines 69-70**: Update filter state from dropdowns
- Gets current selection from each dropdown
- Updates `currentFilter` object

**Line 71**: Re-render with new filters

### Lines 75-81: toggleCompleted() Function

```javascript
function toggleCompleted() {
    showCompleted = !showCompleted;
    const btn = document.getElementById('showCompleted');
    btn.textContent = showCompleted ? 'Hide Completed' : 'Show Completed';
    renderTasks();
}
```

**Line 76**: Toggle boolean
- `!showCompleted`: Flips true ↔ false

**Line 78**: Update button text
- Ternary operator: `condition ? valueIfTrue : valueIfFalse`
- Button text reflects current state

**Line 79**: Re-render with new visibility setting

### Lines 83-91: toggleTask() Function

```javascript
async function toggleTask(taskId) {
    try {
        await eel.toggle_task(taskId)();
        await loadTasks();
    } catch (error) {
        console.error('Error toggling task:', error);
    }
}
```

**Line 85**: Call Python to toggle completion
- Sends task ID to backend
- Python updates task and saves

**Line 86**: Reload tasks
- Refreshes display with updated state

### Lines 93-104: deleteTask() Function

```javascript
async function deleteTask(taskId) {
    if (!confirm('Are you sure you want to delete this task?')) return;
    
    try {
        await eel.delete_task(taskId)();
        await loadTasks();
    } catch (error) {
        console.error('Error deleting task:', error);
        alert('Failed to delete task. Please try again.');
    }
}
```

**Line 94**: Confirmation dialog
- `confirm()`: Browser's built-in confirmation
- Returns `true` if user clicks OK, `false` if Cancel
- Early return if user cancels

**Line 97**: Call Python to delete
- Sends task ID to backend

**Line 98**: Reload tasks
- Removes deleted task from display

### Lines 106-123: editTask() Function

```javascript
function editTask(taskId) {
    const task = tasks.find(t => t.id === taskId);
    if (!task) return;
    
    // Populate form with task data
    document.getElementById('taskTitle').value = task.title;
    document.getElementById('taskDescription').value = task.description || '';
    document.getElementById('taskPriority').value = task.priority;
    document.getElementById('taskDueDate').value = task.due_date || '';
    document.getElementById('taskCategory').value = task.category || '';
    
    // Scroll to form
    document.querySelector('.task-form').scrollIntoView({ behavior: 'smooth' });
    
    // Delete the old task and prepare to add new one
    deleteTask(taskId);
}
```

**Line 107**: Find task in array
- `.find()`: Returns first matching item, or `undefined`
- Arrow function: `t => t.id === taskId`

**Line 108**: Early return if not found
- Prevents errors

**Lines 111-115**: Populate form
- Sets each input's value from task data
- `|| ''`: Default to empty string if value is null/undefined

**Line 118**: Smooth scroll to form
- `scrollIntoView()`: Scrolls element into view
- `behavior: 'smooth'`: Animated scroll

**Line 121**: Delete old task
- User can modify form and submit to create updated task
- **Note**: This is a simple approach. Better would be an "Update" button.

### Lines 125-192: renderTasks() Function

This is the most complex function. Let's break it down:

```javascript
function renderTasks() {
    const container = document.getElementById('tasksContainer');
    
    // Filter tasks
    let filteredTasks = tasks;
    
    // Apply search filter
    if (currentFilter.search) {
        filteredTasks = filteredTasks.filter(task => 
            task.title.toLowerCase().includes(currentFilter.search) ||
            (task.description && task.description.toLowerCase().includes(currentFilter.search)) ||
            (task.category && task.category.toLowerCase().includes(currentFilter.search))
        );
    }
    
    // Apply priority filter
    if (currentFilter.priority) {
        filteredTasks = filteredTasks.filter(task => task.priority === currentFilter.priority);
    }
    
    // Apply category filter
    if (currentFilter.category) {
        filteredTasks = filteredTasks.filter(task => task.category === currentFilter.category);
    }
    
    // Filter completed tasks
    if (!showCompleted) {
        filteredTasks = filteredTasks.filter(task => !task.completed);
    }
    
    // Sort tasks: incomplete first, then by priority, then by due date
    filteredTasks.sort((a, b) => {
        if (a.completed !== b.completed) {
            return a.completed ? 1 : -1;
        }
        const priorityOrder = { high: 3, medium: 2, low: 1 };
        if (priorityOrder[a.priority] !== priorityOrder[b.priority]) {
            return priorityOrder[b.priority] - priorityOrder[a.priority];
        }
        if (a.due_date && b.due_date) {
            return new Date(a.due_date) - new Date(b.due_date);
        }
        if (a.due_date) return -1;
        if (b.due_date) return 1;
        return 0;
    });
    
    // Render
    if (filteredTasks.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <h3>No tasks found</h3>
                <p>${tasks.length === 0 ? 'Add your first task above!' : 'Try adjusting your filters.'}</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = filteredTasks.map(task => createTaskHTML(task)).join('');
    
    // Add event listeners to checkboxes and buttons
    filteredTasks.forEach(task => {
        document.getElementById(`checkbox-${task.id}`).addEventListener('change', () => toggleTask(task.id));
        document.getElementById(`delete-${task.id}`).addEventListener('click', () => deleteTask(task.id));
        document.getElementById(`edit-${task.id}`).addEventListener('click', () => editTask(task.id));
    });
}
```

**Line 128**: Get container element
- Where tasks will be displayed

**Line 131**: Start with all tasks
- Each filter narrows down

**Lines 133-139**: Search filter
- `.filter()`: Creates new array with matching items
- `.includes()`: Checks if string contains substring
- `||`: OR operator (matches if ANY field contains query)

**Lines 142-144**: Priority filter
- Only tasks matching selected priority

**Lines 147-149**: Category filter
- Only tasks matching selected category

**Lines 152-154**: Completed filter
- Hides completed tasks if `showCompleted` is false

**Lines 157-171**: Sorting
- `.sort()`: Sorts array in place
- Comparison function returns:
  - Negative: `a` comes before `b`
  - Positive: `a` comes after `b`
  - Zero: Equal (keep order)
- **Line 159**: Incomplete tasks first
- **Lines 161-164**: Then by priority (high → medium → low)
- **Lines 165-170**: Then by due date (earliest first)

**Lines 174-182**: Empty state
- Shows message if no tasks match filters
- Template literal (backticks) for multi-line string

**Line 184**: Generate HTML
- `.map()`: Transforms each task to HTML string
- `.join('')`: Combines all strings

**Lines 187-191**: Attach event listeners
- Must re-attach after updating HTML
- Arrow functions: `() => toggleTask(task.id)`
- Template literal for ID: `` `checkbox-${task.id}` ``

### Lines 194-219: createTaskHTML() Function

```javascript
function createTaskHTML(task) {
    const isOverdue = task.due_date && !task.completed && new Date(task.due_date) < new Date();
    const dueDateFormatted = task.due_date ? new Date(task.due_date).toLocaleDateString() : '';
    
    return `
        <div class="task-item ${task.completed ? 'completed' : ''}">
            <div class="task-header">
                <input type="checkbox" id="checkbox-${task.id}" class="task-checkbox" ${task.completed ? 'checked' : ''}>
                <div class="task-content">
                    <div class="task-title">${escapeHtml(task.title)}</div>
                    ${task.description ? `<div class="task-description">${escapeHtml(task.description)}</div>` : ''}
                    <div class="task-meta">
                        <span class="task-badge priority-${task.priority}">${task.priority}</span>
                        ${task.category ? `<span class="task-badge category-badge">${escapeHtml(task.category)}</span>` : ''}
                        ${task.due_date ? `<span class="due-date ${isOverdue ? 'overdue' : ''}">📅 ${dueDateFormatted}${isOverdue ? ' (Overdue!)' : ''}</span>` : ''}
                    </div>
                    <div class="task-actions">
                        <button class="btn-edit" id="edit-${task.id}">Edit</button>
                        <button class="btn-delete" id="delete-${task.id}">Delete</button>
                    </div>
                </div>
            </div>
        </div>
    `;
}
```

**Line 196**: Check if overdue
- Has due date AND not completed AND date is in past

**Line 197**: Format date
- Converts "2024-01-15" to "1/15/2024" (locale-specific)

**Line 199**: Template literal
- Backticks allow multi-line strings
- `${}`: Interpolation (inserts values)

**Line 200**: Conditional class
- Adds "completed" class if task is completed
- Used for styling (strikethrough, opacity)

**Line 202**: Checkbox
- `checked` attribute if task is completed
- ID for event listener attachment

**Line 204**: Task title
- `escapeHtml()`: Prevents XSS attacks

**Line 205**: Conditional description
- Only shows if description exists
- Ternary operator for conditional rendering

**Lines 207-210**: Task metadata
- Priority badge with dynamic class
- Category badge (conditional)
- Due date (conditional, with overdue styling)

**Lines 211-214**: Action buttons
- Edit and Delete buttons
- IDs for event listeners

### Lines 221-241: updateCategoryFilter() Function

```javascript
function updateCategoryFilter() {
    const categories = [...new Set(tasks.map(t => t.category).filter(c => c))].sort();
    const select = document.getElementById('filterCategory');
    const currentValue = select.value;
    
    // Keep "All Categories" option
    select.innerHTML = '<option value="">All Categories</option>';
    
    categories.forEach(category => {
        const option = document.createElement('option');
        option.value = category;
        option.textContent = category;
        select.appendChild(option);
    });
    
    // Restore previous selection if it still exists
    if (categories.includes(currentValue)) {
        select.value = currentValue;
    }
}
```

**Line 222**: Extract unique categories
- `tasks.map(t => t.category)`: Gets all categories
- `.filter(c => c)`: Removes empty/null categories
- `new Set(...)`: Removes duplicates
- `[...new Set(...)]`: Converts Set back to array
- `.sort()`: Alphabetical order

**Line 226**: Clear dropdown (except "All Categories")

**Lines 228-233**: Add category options
- `createElement()`: Creates new DOM element
- `appendChild()`: Adds to parent

**Lines 236-238**: Restore selection
- If previously selected category still exists, keep it selected

### Lines 243-248: escapeHtml() Function

```javascript
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
```

**Purpose**: Prevents XSS (Cross-Site Scripting) attacks

**How it works**:
1. Create temporary div element
2. Set `textContent` (automatically escapes HTML)
3. Get `innerHTML` (now safely escaped)
4. `<` becomes `&lt;`, `>` becomes `&gt;`, etc.

**Example**:
- Input: `"<script>alert('hack')</script>"`
- Output: `"&lt;script&gt;alert('hack')&lt;/script&gt;"`
- Browser displays as text, doesn't execute

### Line 251: Application Initialization

```javascript
init();
```

**When it runs**: Immediately when script loads
- Page must be loaded first (scripts at end of HTML)
- Calls `init()` which loads tasks and sets up listeners

---

## index.html - Complete Walkthrough

### Lines 1-8: Document Head

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Intelligent To-Do List</title>
    <link rel="stylesheet" href="style.css">
</head>
```

**Line 1**: HTML5 doctype declaration

**Line 2**: Root element with language attribute

**Line 4**: Character encoding (UTF-8 supports all languages)

**Line 5**: Viewport meta tag (responsive design)

**Line 6**: Page title (browser tab)

**Line 7**: Link to CSS stylesheet

### Lines 10-26: Header Section

```html
<header>
    <h1>✓ Intelligent To-Do List</h1>
    <div class="header-controls">
        <input type="text" id="searchInput" placeholder="Search tasks..." class="search-input">
        <select id="filterPriority" class="filter-select">
            <option value="">All Priorities</option>
            <option value="high">High Priority</option>
            <option value="medium">Medium Priority</option>
            <option value="low">Low Priority</option>
        </select>
        <select id="filterCategory" class="filter-select">
            <option value="">All Categories</option>
        </select>
        <button id="showCompleted" class="btn-toggle">Show Completed</button>
    </div>
</header>
```

**Line 12**: Main heading

**Line 13**: Container for search and filter controls

**Line 14**: Search input
- `type="text"`: Text input field
- `id="searchInput"`: JavaScript identifier
- `placeholder`: Hint text

**Lines 15-20**: Priority filter dropdown
- `select`: Dropdown menu
- `option`: Each choice
- `value=""`: Empty value means "all"

**Lines 21-23**: Category filter (populated dynamically)

**Line 24**: Toggle button for completed tasks

### Lines 28-53: Task Form

```html
<div class="task-form">
    <h2>Add New Task</h2>
    <form id="taskForm">
        <input type="text" id="taskTitle" placeholder="Task title..." required>
        <textarea id="taskDescription" placeholder="Description (optional)"></textarea>
        <div class="form-row">
            <div class="form-group">
                <label for="taskPriority">Priority:</label>
                <select id="taskPriority">
                    <option value="Now">Now</option>
                    <option value="Next" selected>Next</option>
                    <option value="Later">Later</option>
                </select>
            </div>
            <div class="form-group">
                <label for="taskDueDate">Due Date:</label>
                <input type="date" id="taskDueDate">
            </div>
            <div class="form-group">
                <label for="taskCategory">Category:</label>
                <input type="text" id="taskCategory" placeholder="e.g., Work, Personal">
            </div>
        </div>
        <button type="submit" class="btn-primary">Add Task</button>
    </form>
</div>
```

**Line 31**: Form element
- `id="taskForm"`: JavaScript identifier
- Submits when "Add Task" clicked

**Line 32**: Title input
- `required`: Browser validation (can't submit empty)

**Line 33**: Description textarea
- Multi-line text input

**Line 34**: Row container for form fields
- Uses flexbox for layout

**Lines 35-41**: Priority selector
- `selected`: Default option

**Lines 42-45**: Date picker
- `type="date"`: Browser's date picker

**Lines 46-49**: Category text input

**Line 51**: Submit button
- `type="submit"`: Submits form

### Lines 55-60: Tasks Section

```html
<div class="tasks-section">
    <h2>Tasks</h2>
    <div id="tasksContainer" class="tasks-container">
        <!-- Tasks will be dynamically inserted here -->
    </div>
</div>
```

**Line 57**: Container for task list
- `id="tasksContainer"`: JavaScript populates this
- Starts empty, filled by `renderTasks()`

### Lines 63-64: Scripts

```html
<script src="eel.js"></script>
<script src="app.js"></script>
```

**Line 63**: Eel library
- Provided by Eel framework
- Enables Python ↔ JavaScript communication

**Line 64**: Application JavaScript
- Our custom code
- Loaded last (after HTML is parsed)

---

## style.css - Key Concepts

### CSS Selectors

- `*`: Universal selector (all elements)
- `.class-name`: Class selector
- `#id-name`: ID selector
- `element`: Element selector
- `:hover`: Pseudo-class (state-based)

### Layout Systems

- **Flexbox**: `display: flex` for flexible layouts
- **Grid**: `display: grid` for 2D layouts (not used here)

### Common Properties

- `margin`/`padding`: Spacing
- `border`: Borders
- `border-radius`: Rounded corners
- `background`: Colors/gradients
- `color`: Text color
- `font-size`/`font-weight`: Typography
- `transition`: Smooth animations
- `transform`: 2D/3D transformations

### Responsive Design

- `flex-wrap: wrap`: Items wrap on small screens
- `min-width`: Prevents elements from getting too small
- Media queries (not used here, but common for responsive design)

---

This completes the code walkthrough! Use this as a reference while exploring the codebase.

