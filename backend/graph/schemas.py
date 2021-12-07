from marshmallow import Schema, fields


class Query(Schema):
    profundidad = fields.Int(
      default=2,
      description='Profundidad del grafo',
    )


class Metrics(Schema):
    outdegree = fields.Int()
    indegree = fields.Int()
    degree = fields.Int()


class Link(Schema):
    source = fields.Str()
    target = fields.Str()
    tipo = fields.Str()


class Node(Schema):
    _key = fields.Str()
    id = fields.Str()
    nombre = fields.Str()
    subtipo = fields.Str()
    tipo = fields.Str()
    metricas = fields.Nested(Metrics)


class Graph(Schema):
    links = fields.List(fields.Nested(Link))
    nodes = fields.List(fields.Nested(Node))


class GraphResult(Schema):
    execution_time = fields.Float()
    grafo = fields.Nested(Graph)
