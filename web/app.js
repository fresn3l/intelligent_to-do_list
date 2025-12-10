let tasks = [];
let showCompleted = false;
let currentFilter = {
    priority: '',
    category: '',
    search: ''
};

// Initialize the app
async function init() {
    await loadTasks();
    setupEventListeners();
}

// Load tasks from Python backend
async function loadTasks() {
    try {
        tasks = await eel.get_tasks()();
        renderTasks();
        updateCategoryFilter();
    } catch (error) {
        console.error('Error loading tasks:', error);
    }
}

// Setup event listeners
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

// Handle adding a new task
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

// Handle search
function handleSearch(e) {
    currentFilter.search = e.target.value.toLowerCase();
    renderTasks();
}

// Handle filter changes
function handleFilterChange() {
    currentFilter.priority = document.getElementById('filterPriority').value;
    currentFilter.category = document.getElementById('filterCategory').value;
    renderTasks();
}

// Toggle showing completed tasks
function toggleCompleted() {
    showCompleted = !showCompleted;
    const btn = document.getElementById('showCompleted');
    btn.textContent = showCompleted ? 'Hide Completed' : 'Show Completed';
    renderTasks();
}

// Toggle task completion
async function toggleTask(taskId) {
    try {
        await eel.toggle_task(taskId)();
        await loadTasks();
    } catch (error) {
        console.error('Error toggling task:', error);
    }
}

// Delete task
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

// Edit task
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

// Render tasks
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

// Create HTML for a task
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

// Update category filter dropdown
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

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Initialize when page loads
init();

