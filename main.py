from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    with sqlite3.connect("tasks.db") as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'Pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
init_db()

# Home page - list tasks
@app.route('/')
def index():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)

# Add task
@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    with sqlite3.connect("tasks.db") as conn:
        conn.execute("INSERT INTO tasks (title, description) VALUES (?, ?)", (title, description))
    return redirect(url_for('index'))

# Update task status
@app.route('/update/<int:id>')
def update_task(id):
    with sqlite3.connect("tasks.db") as conn:
        conn.execute("UPDATE tasks SET status = CASE WHEN status='Pending' THEN 'Completed' ELSE 'Pending' END WHERE id=?", (id,))
    return redirect(url_for('index'))

# Delete task
@app.route('/delete/<int:id>')
def delete_task(id):
    with sqlite3.connect("tasks.db") as conn:
        conn.execute("DELETE FROM tasks WHERE id=?", (id,))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
