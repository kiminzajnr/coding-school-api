from db import db


class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unque=False, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("courses.id", nullable=False))

    course = db.relationship("CourseModel", back_populates="tags")