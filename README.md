# ToDo - Habit Tracker

A beautiful desktop application for tracking habits and goals, built with Python (Eel) and modern web technologies.

## 📚 Learning Resources

This repository includes comprehensive documentation:

- **[MODULE_STRUCTURE.md](MODULE_STRUCTURE.md)**: Detailed explanation of the modular architecture

Perfect for learning Python, JavaScript, HTML, CSS, and desktop app development!

## Features

- ✨ **Modern UI**: Beautiful gradient design with smooth animations
- 📝 **Habit Tracking**: Add, edit, delete, and check in habits
- 🎯 **Priority Levels**: Organize habits by priority (Now, Next, Later, Today, Someday)
- ⏱️ **Time Tracking**: Optional time tracking for habits (e.g., workouts, reading)
- 🔥 **Streaks**: Track your habit streaks and consistency
- 📊 **Analytics**: Comprehensive analytics including time analytics with visualizations
- 🎯 **Goals**: Link habits to goals and track progress
- 🔍 **Search & Filter**: Quickly find habits by searching or filtering
- 💾 **Local Storage**: All data is saved locally in Application Support folder
- ✅ **Smart Sorting**: Habits are automatically sorted by goal and priority

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

### Development Mode

Run the application:
```bash
python main.py
```

### Building a Standalone Mac App

To create a standalone Mac application that doesn't require Python:

1. **Install PyInstaller**:
```bash
pip install pyinstaller
```

2. **Build the app**:
```bash
python build_app.py
```

3. **Find your app**:
   - Location: `dist/ToDo/ToDo.app` or automatically copied to `/Applications/ToDo.app`
   - Double-click to run!

The application will open in a desktop window where you can:
- Add new habits with title, description, priority, frequency, and optional goal
- Enable time tracking for habits that require it
- Check in habits daily and optionally record time spent
- Search habits using the search bar
- Filter habits by priority, frequency, or goal
- View habit streaks and 7-day history
- Edit or delete existing habits
- Create and manage goals
- View comprehensive analytics including time analytics

## Data Storage

All habits and goals are stored locally in your Application Support folder:
- `habits.json` - All habit data including check-ins and time tracking
- `goals.json` - All goal data

Your data persists between sessions and app rebuilds.

## Project Structure

```
intelligent_to-do_list/
├── main.py              # Application entry point
├── habits.py            # Habit management functions
├── goals.py             # Goal management functions
├── analytics.py         # Analytics and statistics
├── data_storage.py      # File I/O operations
├── build_app.py         # Build script for creating .app
├── requirements.txt     # Python dependencies
├── app_icon.icns        # Application icon
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

