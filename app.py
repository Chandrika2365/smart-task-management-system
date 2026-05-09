from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import numpy as np

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'

# SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskdb.db'

db = SQLAlchemy(app)

# Task Table
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(200))
    priority = db.Column(db.String(50))
    status = db.Column(db.String(50))

@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':

        title = request.form['title']
        description = request.form['description']
        priority = request.form['priority']
        status = request.form['status']

        new_task = Task(
            title=title,
            description=description,
            priority=priority,
            status=status
        )

        db.session.add(new_task)
        db.session.commit()

        return redirect('/')

    tasks = Task.query.all()

    task_list = []

    for task in tasks:
        task_list.append({
            'status': task.status
        })

    df = pd.DataFrame(task_list, columns=['status'])

    total_tasks = len(df)

    completed_tasks = len(df[df['status'] == 'Completed'])

    pending_tasks = len(df[df['status'] == 'Pending'])

    if total_tasks > 0:
        completion_percentage = np.round((completed_tasks / total_tasks) * 100, 2)
    else:
        completion_percentage = 0

    return render_template(
        'index.html',
        tasks=tasks,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        completion_percentage=completion_percentage
    )

# DELETE TASK
@app.route('/delete/<int:id>')
def delete(id):

    task = Task.query.get(id)

    db.session.delete(task)

    db.session.commit()

    return redirect('/')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):

    task = Task.query.get(id)

    if request.method == 'POST':

        task.title = request.form['title']
        task.description = request.form['description']
        task.priority = request.form['priority']
        task.status = request.form['status']

        db.session.commit()

        return redirect('/')

    return render_template('update.html', task=task)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)