from flask_smorest import Blueprint, abort

from flask.views import MethodView

from models import ProjectModel

from db import db

from sqlalchemy.exc import SQLAlchemyError

from schemas import ProjectSchema, ProjectUpdateSchema

blp = Blueprint("Projects", __name__, description="Operations on projects")


@blp.route("/project/<string:project_id>")
class Project(MethodView):
    @blp.response(200, ProjectSchema)
    def get(self, project_id):
        try:
            return projects[project_id]
        except KeyError:
            abort(404, message="Project not found.")

    def delete(self, project_id):
        try:
            del projects[project_id]
            return {"message": "Project deleted."}
        except KeyError:
            abort(404, message="Project not found.")

    @blp.arguments(ProjectUpdateSchema)
    @blp.response(200, ProjectSchema)
    def put(self, project_data, project_id):
        try:
            project = projects[project_id]
            project |= project_data

            return project
        
        except KeyError:
            abort(404, message="Project not found.")

@blp.route("/project")
class ProjectList(MethodView):
    @blp.response(200, ProjectSchema(many=True))
    def get(self):
        return {"project": list(projects.values())}
    
    @blp.arguments(ProjectSchema)
    @blp.response(201, ProjectSchema)
    def post(self, project_data):
        project = ProjectModel(**project_data)

        try:
            db.session.add(project)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the project")

        return project
