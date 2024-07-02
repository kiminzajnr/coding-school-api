from flask import Flask, request

app = Flask(__name__)

courses = [
    {
        "name": "My Course 1", "projects": [
            {
                "name": "My Project 1", "description": "My favourite project"
            },
            {
                "name": "My Project 1", "description": "My favourite project"
            }
        ]
    }
]

@app.get("/course")
def get_courses():
    return {"courses": courses}

@app.post("/course")
def create_course():
    request_data = request.get_json()
    new_course = {"name": request_data["name"], "projects": []}
    courses.append(new_course)
    return new_course, 201

@app.post("/course/<string:name>/project")
def create_project(name):
    request_data = request.get_json()
    for course in courses:
        if course["name"] == name:
            new_project = {"name": request_data["name"], "description": request_data["description"]}
            course["projects"].append(new_project)
            return new_project
        
    return {"message": "Course not found"}, 404