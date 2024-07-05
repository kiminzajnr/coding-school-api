from db import db


class TaskModel(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    description = db.Column(db.String(1000), nullable=False)

    project_id = db.Column(
        db.Integer, db.ForeignKey("projects.id"), unique=False, nullable=False
    )

    projects = db.relationship("ProjectModel", back_populates="tasks")