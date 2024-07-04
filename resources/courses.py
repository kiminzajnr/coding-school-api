import uuid

from flask_smorest import Blueprint, abort

from flask.views import MethodView
from flask import request

from db import courses
from schemas import CourseSchema


blp = Blueprint("Courses", __name__, description="Operations on courses")


@blp.route("/course/<string:course_id>")
class Course(MethodView):
    @blp.response(200, CourseSchema)
    def get(self, course_id):
        try:
            return courses[course_id]
        except KeyError:
            abort(404, message="Course not found.")

    def delete(self, course_id):
        try:
            del courses[course_id]
            return {"message": "Course deleted."}
        except KeyError:
            abort(404, message="Course not found.")


@blp.route("/course")
class CourseList(MethodView):
    @blp.response(200, CourseSchema(many=True))
    def get(self):
        return {"courses": list(courses.values())}
    
    @blp.arguments(CourseSchema)
    @blp.response(201, Course)
    def post(self, course_data):
        course_id = uuid.uuid4().hex
        course = {**course_data, "id": course_id}
        courses[course_id] = course

        return course, 201