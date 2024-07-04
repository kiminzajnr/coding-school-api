from marshmallow import Schema, fields


class ProjectSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    course_id = fields.Str(required=True)

class ProjectUpdateSchema(Schema):
    name = fields.Str()
    description = fields.Str()

class CourseSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)