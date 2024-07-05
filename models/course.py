from db import db


class CourseModel(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), unique=True, nullable=False)

    projects = db.relationship("ProjectModel", back_populates="course", lazy="dynamic", cascade="all, delete")