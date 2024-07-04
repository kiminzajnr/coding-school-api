from marshmallow import Schema, fields


class PlainProjectSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)

class PlainCourseSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)

class ProjectSchema(PlainProjectSchema):
    course_id = fields.Int(required=True, load_only=True)
    course = fields.Nested(PlainCourseSchema(), dump_only=True)

class ProjectUpdateSchema(Schema):
    name = fields.Str()
    description = fields.Str()

class CourseSchema(PlainCourseSchema):
    projects = fields.List(fields.Nested(PlainProjectSchema()), dump_only=True)
