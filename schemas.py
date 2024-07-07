from marshmallow import Schema, fields


class PlainTaskSchema(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)

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
    tasks = fields.List(fields.Nested(PlainTaskSchema()), dump_only=True)

class TaskSchema(PlainTaskSchema):
    project_id = fields.Int(required=True, load_only=True)
    project = fields.Nested(PlainProjectSchema(), dump_only=True)

class ProjectUpdateSchema(Schema):
    name = fields.Str()
    description = fields.Str()
    course_id = fields.Int()

class TaskUpdateSchema(Schema):
    title = fields.Str()
    description = fields.Str()
    project_id = fields.Int()

class CourseSchema(PlainCourseSchema):
    projects = fields.List(fields.Nested(PlainProjectSchema()), dump_only=True)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
