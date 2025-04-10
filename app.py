from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todolist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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
    with app.app_context():
        db.create_all()
    app.run(debug=True)
