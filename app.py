import uuid

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
    project_id = uuid.uuid4.hex
    project = {**project_data, "id": project_id}
    projects[project_id] = project

    return project
    
@app.get("/course/<string:course_id>")
def get_course(course_id):
    try:
        return courses[course_id]
    except KeyError:
        return {"message": "Course not found"}, 404

@app.get("/course/<string:project_id")
def get_project_in_course(project_id):
    try:
        return projects[project_id]
    except KeyError:
        return {"message": "Project not found"}, 404