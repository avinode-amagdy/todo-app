from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

# Database configuration
DATABASE = 'todos.db'

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database"""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            completed BOOLEAN NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Main page showing all todos"""
    conn = get_db_connection()
    todos = conn.execute(
        'SELECT * FROM todos ORDER BY created_at DESC'
    ).fetchall()
    conn.close()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    """Add a new todo"""
    title = request.form['title']
    description = request.form.get('description', '')
    
    if title:
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO todos (title, description) VALUES (?, ?)',
            (title, description)
        )
        conn.commit()
        conn.close()
    
    return redirect(url_for('index'))

@app.route('/toggle/<int:todo_id>')
def toggle_todo(todo_id):
    """Toggle todo completion status"""
    conn = get_db_connection()
    todo = conn.execute(
        'SELECT * FROM todos WHERE id = ?', (todo_id,)
    ).fetchone()
    
    if todo:
        new_status = not todo['completed']
        conn.execute(
            'UPDATE todos SET completed = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
            (new_status, todo_id)
        )
        conn.commit()
    
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    """Delete a todo"""
    conn = get_db_connection()
    conn.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/api/todos')
def api_todos():
    """API endpoint to get all todos as JSON"""
    conn = get_db_connection()
    todos = conn.execute(
        'SELECT * FROM todos ORDER BY created_at DESC'
    ).fetchall()
    conn.close()
    
    todos_list = []
    for todo in todos:
        todos_list.append({
            'id': todo['id'],
            'title': todo['title'],
            'description': todo['description'],
            'completed': bool(todo['completed']),
            'created_at': todo['created_at'],
            'updated_at': todo['updated_at']
        })
    
    return jsonify(todos_list)

@app.route('/health')
def health_check():
    """Health check endpoint for Kubernetes"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
