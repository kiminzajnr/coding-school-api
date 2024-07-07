from flask_smorest import Blueprint, abort

from flask_jwt_extended import jwt_required

from flask.views import MethodView

from sqlalchemy.exc import SQLAlchemyError

from schemas import TaskSchema, TaskUpdateSchema

from models import TaskModel

from db import db


blp = Blueprint("Tasks", __name__, description="Operations on tasks")


@blp.route("/task/<int:task_id>")
class Task(MethodView):
    @blp.response(200, TaskSchema)
    def get(self, task_id):
        task = TaskModel.query.get_or_404(task_id)

        return task
    
    @jwt_required()
    def delete(self, task_id):
        task = TaskModel.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()

        return {"message": "Task deleted successfully."}, 200
    
    @jwt_required()
    @blp.arguments(TaskUpdateSchema)
    @blp.response(200, TaskSchema)
    def put(self, task_data, task_id):
        task = TaskModel.query.get(task_id)
        if task:
            task.title = task_data["title"]
            task.description = task_data["description"]

        else:
            task = TaskModel(id=task_id, **task_data)

        db.session.add(task)
        db.session.commit()

        return task

@blp.route("/task")
class TaskList(MethodView):
    @blp.response(200, TaskSchema(many=True))
    def get(self):
        return TaskModel.query.all()
    
    @jwt_required()
    @blp.arguments(TaskSchema)
    @blp.response(201, TaskSchema)
    def post(self, task_data):
        task = TaskModel(**task_data)
        try:
            db.session.add(task)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the task")

        return task