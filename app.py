from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime
import os

app = Flask(__name__)

# Check for Render's persistent disk path (for SQLite)
# You can switch to PostgreSQL later if needed
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:////mnt/data/todolist.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and migration tools
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Todo(db.Model):
    Serial_No = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(400), nullable=False)
    describe = db.Column(db.String(900), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __str__(self):
        return f"{self.Serial_No} - {self.title}"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        describe = request.form['describe']
        new_task = Todo(title=title, describe=describe)
        db.session.add(new_task)
        db.session.commit()
        return redirect('/')

    all_tasks = Todo.query.order_by(Todo.date_created.desc()).all()
    return render_template('index.html', tasks=all_tasks)

@app.route('/delete/<int:serial_no>')
def delete(serial_no):
    task_to_delete = Todo.query.get_or_404(serial_no)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    # This will only create the tables if they don't already exist
    with app.app_context():
        db.create_all()  # db.create_all() is useful for SQLite but Flask-Migrate is more flexible for larger apps

    app.run(debug=True)
