from db import db


class ProjectsTags(db.Model):
    __tablename__ = "projects_tags"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))