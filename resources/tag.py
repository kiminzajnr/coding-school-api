from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from schemas import TagSchema
from models import TagModel, CourseModel
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