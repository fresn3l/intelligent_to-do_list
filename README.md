# Intelligent To-Do List

A beautiful desktop application for managing your tasks, built with Python (Eel) and modern web technologies.

## 📚 Learning Resources

This repository includes comprehensive educational documentation:

- **[LEARNING_GUIDE.md](LEARNING_GUIDE.md)**: Complete tutorial teaching you how to code through this project
- **[CODE_WALKTHROUGH.md](CODE_WALKTHROUGH.md)**: Line-by-line code explanations for every file

Perfect for beginners learning Python, JavaScript, HTML, CSS, and desktop app development!

## Features

- ✨ **Modern UI**: Beautiful gradient design with smooth animations
- 📝 **Task Management**: Add, edit, delete, and complete tasks
- 🎯 **Priority Levels**: Organize tasks by priority (High, Medium, Low)
- 📅 **Due Dates**: Set and track due dates with overdue indicators
- 🏷️ **Categories**: Organize tasks by category
- 🔍 **Search & Filter**: Quickly find tasks by searching or filtering
- 💾 **Local Storage**: All data is saved locally in `tasks.json`
- ✅ **Smart Sorting**: Tasks are automatically sorted by completion status, priority, and due date

## Installation

### Recommended: Using a Virtual Environment

1. Create a virtual environment:
```bash
python3 -m venv venv
```

2. Activate the virtual environment:
   - **macOS/Linux**: `source venv/bin/activate`
   - **Windows**: `venv\Scripts\activate`

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. When you're done working, deactivate the virtual environment:
```bash
deactivate
```

### Alternative: Global Installation (Not Recommended)

If you prefer to install globally (not recommended for most cases):
```bash
pip install -r requirements.txt
```

**Note**: Using a virtual environment is strongly recommended to avoid conflicts with other Python projects and keep your system Python clean.

## Usage

Run the application:
```bash
python main.py
```

The application will open in a desktop window where you can:
- Add new tasks with title, description, priority, due date, and category
- Search tasks using the search bar
- Filter tasks by priority or category
- Toggle task completion
- Edit or delete existing tasks
- View completed tasks (toggle with the "Show Completed" button)

## Data Storage

All tasks are stored locally in `tasks.json` in the application directory. Your data persists between sessions.

## Project Structure

```
intelligent_to-do_list/
├── main.py              # Python backend with Eel
├── requirements.txt     # Python dependencies
├── tasks.json          # Local data storage (created automatically)
└── web/
    ├── index.html      # Main HTML file
    ├── style.css       # Styling
    └── app.js          # Frontend JavaScript logic
```

## Technologies

- **Python 3**: Backend logic
- **Eel**: Desktop app framework
- **HTML/CSS/JavaScript**: Frontend interface
- **JSON**: Local data storage

