import uuid

from flask_smorest import Blueprint, abort

from flask.views import MethodView
from flask import request

from db import courses


blp = Blueprint("courses", __name__, description="Operations on courses")


@blp.route("/course/<string:course_id>")
class Course(MethodView):
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
    def get(self):
        return {"courses": list(courses.values())}
    
    def post(self):
        course_data = request.get_json()
        course_id = uuid.uuid4().hex
        course = {**course_data, "id": course_id}
        courses[course_id] = course
        
        return course, 201