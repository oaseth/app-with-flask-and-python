from flask import Flask, render_template, request, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

# Initialize a flask app
app = Flask(__name__)

# Add the config file
app.config.from_pyfile('config.py')

# The db
db = SQLAlchemy(app)


class Project(db.Model):
    """
    A model for the "Project" table
    """
    __tablename__ = "projects"

    # The columns of the table
    project_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(length=60))

    # The relationship of this model with the task model
    task = db.relationship("Task", cascade="all, delete-orphan")


class Task(db.Model):
    """
    A model for the "Task" table
    """
    __tablename__ = "tasks"

    # The columns of the table
    task_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.project_id"))
    description = db.Column(db.String(60))

    # The relationship of this model with the project model
    project = db.relationship("Project", backref="project")


@app.route("/")
def show_projects():
    """
    A function to display projects
    """
    return render_template("index.html", projects=Project.query.all())


@app.route("/project/<project_id>")
def show_tasks(project_id):
    """
    A function to display the tasks of a particular project

    Parameter
    ---------
        project_id: the ID of the project to be displayed
    """
    return render_template("project-tasks.html",
                           project=Project.query.filter_by(
                               project_id=project_id).first(),
                           tasks=Task.query.filter_by(project_id=project_id).all())


@app.route("/add/project", methods=['post'])
def add_project():
    """
    A function to add a new project
    """
    if not request.form["project-title"]:
        flash("Enter a title for your new project", "red")
    else:
        project = Project(title=request.form["project-title"])
        db.session.add(project)
        db.session.commit()
        flash("Project added successfully", "green")
    return redirect(url_for("show_projects"))


@app.route("/add/task/<project_id>", methods=['post'])
def add_task(project_id):
    """
    A function to add a new task to a particular project

    Parameter
    ---------
        project_id: the ID of the project to add the task to
    """
    if not request.form["task-description"]:
        flash("Enter a description for your new task", "red")
    else:
        task = Task(
            description=request.form["task-description"], project_id=project_id)
        db.session.add(task)
        db.session.commit()
        flash("Task added successfully", "green")
    return redirect(url_for("show_tasks", project_id=project_id))


@app.route("/delete/task/<task_id>", methods=['post'])
def delete_task(task_id):
    """
    A function to delete a task

    Parameter
    ---------
        task_id: the ID of the task to delete
    """
    pending_delete_task = Task.query.filter_by(task_id=task_id).first()
    orig_project_id = pending_delete_task.project.project_id
    db.session.delete(pending_delete_task)
    db.session.commit()
    return redirect(url_for("show_tasks", project_id=orig_project_id))


@app.route("/delete/project/<project_id>", methods=['post'])
def delete_project(project_id):
    """
    A function to delete a project

    Parameter
    ---------
        project_id: the ID of the project to delete
    """
    pending_delete_project = Project.query.filter_by(
        project_id=project_id).first()
    db.session.delete(pending_delete_project)
    db.session.commit()
    return redirect(url_for("show_projects"))


# Run Flask app
app.run(debug=True, host="localhost", port=3000)
