from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from schemas import TagSchema, TagAndProjectSchema
from models import TagModel, CourseModel, ProjectModel
from db import db


blp = Blueprint("Tags", "tags", description="Operations on tags")


@blp.route("/course/<int:course_id>/tag")
class TagInCourse(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, course_id):
        course = CourseModel.query.get_or_404(course_id)

        return course.tags.all()
    
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, course_id):
        if TagModel.query.filter(TagModel.course_id == course_id, TagModel.name == tag_data["name"]).first():
            abort(400, message="A tag with that name already exists in that store.")

        tag = TagModel(**tag_data, course_id=course_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(
                500,
                message=str(e),
            )

        return tag
    

@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        return tag
    
    @blp.response(
        202,
        description="Deletes a tag if no project is tagged with it.",
        example={"message": "Tag deleted."},
    )
    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(
        400,
        description="Returned if the tag is assigned to one or more projects. In this case the tag is not deleted.",
    )
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.projects:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted."}
        abort(
            400,
            message="Could not delete tag. Make sure the tag is not associated with any projects then try again.",
        )
    

@blp.route("/project/<int:project_id>/tag/<int:tag_id>")
class LinkTagsToProject(MethodView):
    @blp.response(201, TagSchema)
    def post(self, project_id, tag_id):
        project = ProjectModel.query.get_or_404(project_id)
        tag = TagModel.query.get_or_404(tag_id)

        project.tags.append(tag)

        try:
            db.session.add(project)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")

        return tag
    
    @blp.response(200, TagAndProjectSchema)
    def delete(self, project_id, tag_id):
        project = ProjectModel.query.get_or_404(project_id)
        tag = TagModel.query.get_or_404(tag_id)

        project.tags.remove(tag)

        try:
            db.session.add(project)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")
        
        return {"message": "Project removed from tag", "project": project, "tag": tag}
    