from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Todo
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        todo = request.form.get('note')#Gets the todo from the HTML 

        if len(todo) < 1:
            flash('Todo is too short!', category='error') 
        else:
            new_todo = Todo(data=todo, user_id=current_user.id)  #providing the schema for the todo 
            db.session.add(new_todo) #adding the todo to the database 
            db.session.commit()
            flash('Todo added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-todo', methods=['POST'])
def delete_todo():  
    todo = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    todoId = todo['noteId']
    todo = Todo.query.get(todoId)
    if todo:
        if todo.user_id == current_user.id:
            db.session.delete(todo)
            db.session.commit()

    return jsonify({})
