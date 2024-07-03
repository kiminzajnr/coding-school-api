import uuid

from flask_smorest import abort
from flask import Flask, request

from db import courses, projects

app = Flask(__name__)


@app.get("/course")
def get_courses():
    return {"courses": list(courses.values())}

@app.get("/project")
def get_projects():
    return {"projects": list(projects.values())}

@app.post("/course")
def create_course():
    course_data = request.get_json()
    course_id = uuid.uuid4().hex
    course = {**course_data, "id": course_id}
    courses[course_id] = course
    return course, 201

@app.post("/project")
def create_project():
    project_data = request.get_json()
    if project_data["course_id"] not in courses:
        return {"message": "Course not found"}, 404
    project_id = uuid.uuid4().hex
    project = {**project_data, "id": project_id}
    projects[project_id] = project

    return project
    
@app.get("/course/<string:course_id>")
def get_course(course_id):
    try:
        return courses[course_id]
    except KeyError:
        abort(404, message="Course not found.")

@app.get("/project/<string:project_id>")
def get_project(project_id):
    try:
        return projects[project_id]
    except KeyError:
        abort(404, message="Project not found.")

@app.delete("/project/<string:project_id>")
def delete_project(project_id):
    try:
        del projects[project_id]
        return {"message": "Project deleted."}
    except KeyError:
        abort(404, message="Project not found.")

@app.put("/project/<string:project_id>")
def update_project(project_id):
    project_data = request.get_json()
    try:
        project = projects[project_id]
        project |= project_data

        return project
    
    except KeyError:
        abort(404, message="Project not found.")

@app.delete("/course/<string:course_id>")
def delete_course(course_id):
    try:
        del courses[course_id]
        return {"message": "Course deleted."}
    except KeyError:
        abort(404, message="Course not found.")