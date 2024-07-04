import uuid

from flask_smorest import Blueprint, abort

from flask.views import MethodView
from flask import request

from db import projects

from schemas import ProjectSchema

blp = Blueprint("Projects", __name__, description="Operations on projects")


@blp.route("/project/<string:project_id>")
class Project(MethodView):
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

    @blp.arguments(ProjectSchema)
    def put(self, project_data, project_id):
        try:
            project = projects[project_id]
            project |= project_data

            return project
        
        except KeyError:
            abort(404, message="Project not found.")

@blp.route("/project")
class ProjectList(MethodView):
    def get(self):
        return {"project": list(projects.values())}
    
    @blp.arguments(ProjectSchema)
    def post(self, project_data):
        project_id = uuid.uuid4().hex
        project = {**project_data, "id": project_id}
        projects[project_id] = project

        return project
