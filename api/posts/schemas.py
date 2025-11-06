from marshmallow import Schema, fields

class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    user_id = fields.Int(dump_only=True)
    
post_schema = PostSchema()
posts_schema = PostSchema(many=True)