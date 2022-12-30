from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 
app = Flask(__name__);
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///todo.db'
db = SQLAlchemy(app)
class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500),nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        task_content = request.form["content"]
        print(task_content)
        new_task = ToDo(content=task_content)
        print(new_task)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except BaseException as error:
            print('An Error occurred: {}'.format(error))

    else: 
        tasks = ToDo.query.order_by(ToDo.date_created).all()
        return render_template("index.html", tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = ToDo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except BaseException as error:
        print('An Error occurred while deleting: {}'.format(error))

@app.route('/update/<int:id>',methods=["POST",'GET'])
def update(id):
    task = ToDo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form["content"]

        try:
            db.session.commit()
            return redirect("/")
        except BaseException as error:
            print('An Error occurred while deleting: {}'.format(error))

    else:
        return render_template("update.html",task=task)


if __name__ == "__main__":
    app.run(debug=True)