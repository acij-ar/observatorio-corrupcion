from marshmallow import Schema, fields, validate


class Query(Schema):
    q = fields.Str(required=True)
    limit = fields.Int(default=10, validate=validate.Range(min=1, max=50))

class Result(Schema):
    degree = fields.Int()
    key = fields.Str()
    nombre = fields.Str()
    sub_tipo = fields.Str()
    tipo = fields.Str()

class Search(Schema):
    execution_time = fields.Float()
    results = fields.List(fields.Nested(Result))
