from db import db


class ProjectModel(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    description = db.Column(db.String(1000), nullable=False)

    course_id = db.Column(
        db.Integer, db.ForeignKey("courses.id"), unique=False, nullable=False
    )
    course = db.relationship("CourseModel", back_populates="projects")

    tasks = db.relationship("TaskModel", back_populates="project", lazy="dynamic", cascade="all, delete")

    tags = db.relationship("TagModel", back_populates="projects", secondary="projects_tags")