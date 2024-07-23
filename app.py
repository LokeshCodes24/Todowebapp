from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Sample data stores (in-memory)
tasks = []
users = []

# Routes
@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('task_manager'))
    return redirect(url_for('get_started'))

@app.route('/get_started', methods=['GET', 'POST'])
def get_started():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        for user in users:
            if user['email'] == email and user['password'] == password:
                session['username'] = user['username']
                flash('Login successful!', 'success')
                return redirect(url_for('task_manager'))
        flash('Invalid email or password. Please try again.', 'danger')
        return redirect(url_for('login'))
    return render_template('get_started.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        users.append({'username': username, 'email': email, 'password': password})
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        for user in users:
            if user['email'] == email and user['password'] == password:
                session['username'] = user['username']
                flash('Login successful!', 'success')
                return redirect(url_for('task_manager'))
        flash('Invalid email or password. Please try again.', 'danger')
        return render_template('login.html', error='Invalid email or password. Please try again.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/task_manager')
def task_manager():
    if 'username' in session:
        return render_template('index.html', tasks=tasks, username=session['username'])
    return redirect(url_for('login'))

@app.route('/add_task', methods=['POST'])
def add_task():
    task = request.form.get('task')
    due_date = 'today' 
    if task:
        tasks.append({'task': task, 'due_date': due_date, 'completed': False})
        flash('Task added successfully!', 'success')
    return redirect(url_for('task_manager'))

@app.route('/complete_task/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks[task_id]['completed'] = True
        flash('Task completed!', 'success')
    return redirect(url_for('task_manager'))

@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        del tasks[task_id]
        flash('Task deleted!', 'danger')
    return redirect(url_for('task_manager'))

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    if task_id < 0 or task_id >= len(tasks):
        return redirect(url_for('task_manager'))

    if request.method == 'POST':
        new_task = request.form.get('task')
        tasks[task_id]['task'] = new_task
        flash('Task updated successfully!', 'info')
        return redirect(url_for('task_manager'))

    return render_template('edit.html', task_id=task_id, task=tasks[task_id]['task'])

@app.route('/today_tasks')
def today_tasks():
    today = datetime.now().date()
    today_tasks = [task for task in tasks if task['due_date'] == 'today' and not task['completed']]
    return render_template('today_tasks.html', tasks=today_tasks)

@app.route('/scheduled_tasks')
def scheduled_tasks():
    scheduled_tasks = [task for task in tasks if task['due_date'] != 'today' and not task['completed']]
    return render_template('scheduled_tasks.html', tasks=scheduled_tasks)

@app.route('/completed_tasks')
def complete_tasks():
    complete_tasks = [task for task in tasks if task['completed']]
    return render_template('completed_tasks.html', tasks=complete_tasks)

if __name__ == '__main__':
    app.run(debug=True)
