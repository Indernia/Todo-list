from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    completed = db.Column(db.Boolean, default=False)




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

todos = ()
@app.route('/')
def index():
    with app.app_context():
        todos = Todo.query.all()
        titles = [todo.title for todo in todos if not todo.completed]
        done = [todo.title for todo in todos if todo.completed]
    return render_template('index.html', titles=titles, done=done)

@app.route('/add_todo', methods=['POST'])
def add_todo():
    todo = request.form.get('todo')
    db.session.add(Todo(title=todo))
    db.session.commit()
    return redirect('/')


@app.route('/delete_todo', methods=['POST'])
def delete_todo():
    id = int(request.form.get('index'))
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


@app.route('/delete_todo_name', methods=['POST'])
def delete_todo_name():
    title = request.form.get('todo_text')
    print(title)
    todo = Todo.query.filter_by(title=title).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


@app.route('/completed', methods=['POST'])
def completed():
    title = request.form.get('completed')
    print(title)
    todo = Todo.query.filter_by(title=title).first()
    todo.completed = True
    db.session.commit()
    return redirect('/')


@app.route('/uncompleted', methods=['POST'])
def uncompleted():
    title = request.form.get('uncompleted')
    print(title)
    todo = Todo.query.filter_by(title=title).first()
    todo.completed = False
    db.session.commit()
    return redirect('/')