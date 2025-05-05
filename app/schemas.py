from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str()
    due_date = fields.DateTime()
    is_completed = fields.Bool()
    priority = fields.Str()
    user_id = fields.Int(dump_only=True)
    category_id = fields.Int()

class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    user_id = fields.Int(dump_only=True)
