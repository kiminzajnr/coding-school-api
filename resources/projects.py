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
        project = ProjectModel.query.get_or_404(project_id)
        return project

    def delete(self, project_id):
        project = ProjectModel.query.get_or_404(project_id)
        db.session.delete(project)
        db.session.commit()
        return {"message": "Project deleted."}, 200

    @blp.arguments(ProjectUpdateSchema)
    @blp.response(200, ProjectSchema)
    def put(self, project_data, project_id):
        project = ProjectModel.query.get(project_id)
        if project:
            project.name = project_data["name"]
            project.description = project_data["description"]
        else:
            project = ProjectModel(id=project_id, **project_data)
        
        db.session.add(project)
        db.session.commit()

        return project

@blp.route("/project")
class ProjectList(MethodView):
    @blp.response(200, ProjectSchema(many=True))
    def get(self):
        return ProjectModel.query.all()
    
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
