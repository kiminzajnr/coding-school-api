from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from flask_jwt_extended import get_jwt

from flask_jwt_extended import jwt_required

from flask_smorest import Blueprint, abort

from flask.views import MethodView

from db import db

from models import CourseModel

from schemas import CourseSchema


blp = Blueprint("Courses", __name__, description="Operations on courses")


@blp.route("/course/<string:course_id>")
class Course(MethodView):
    @blp.response(200, CourseSchema)
    def get(self, course_id):
        course = CourseModel.query.get_or_404(course_id)
        return course

    @jwt_required()
    def delete(self, course_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required!")
        course = CourseModel.query.get_or_404(course_id)
        db.session.delete(course)
        db.session.commit()
        return {"message": "Course deleted"}, 200
        


@blp.route("/course")
class CourseList(MethodView):
    @blp.response(200, CourseSchema(many=True))
    def get(self):
        return CourseModel.query.all()
    
    @jwt_required()
    @blp.arguments(CourseSchema)
    @blp.response(201, CourseSchema)
    def post(self, course_data):
        course = CourseModel(**course_data)

        try:
            db.session.add(course)
            db.session.commit()
        except IntegrityError:
            abort(
                404,
                message="A course with that name already exists.",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the course.")

        return course, 201