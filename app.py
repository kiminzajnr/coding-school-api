from flask import Flask

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