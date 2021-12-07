from flask_restful import Resource, abort
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource

from plugins import cache
from session import arangoDB
from graph import schemas


class Graph(MethodResource, Resource):
    valid_collections = [
        'nodos_causas',
        'nodos_entidades',
        'nodos_magistrados',
    ]

    @doc(description='Grafo', tags=['Grafo'])
    @use_kwargs(schemas.Query, location="query")
    @marshal_with(schemas.GraphResult)
    @cache.cached(query_string=True)
    def get(self, collection, document, profundidad=2):
        # Check if the collection is valid
        if collection not in self.valid_collections:
            abort(404, message=f'La coleccion "{collection}" no existe')

        args = {
            'node': collection + '/' + document.replace(' ', '_'),
            'profundidad': profundidad,
        }
        result = query_graph(args)

        # Check if the node name is valid
        if not result['grafo']['nodes']:
            abort(404, message=f'El nodo "{document}" no existe')

        return result


def query_graph(parameters):
    query1 = """
    LET nodes = (
        FOR v, e, p IN 0..@deep ANY @node GRAPH "grafo"
            PRUNE v.nombre == 'DEFENSORIA PUBLICA OFICIAL'
            OPTIONS {bfs: true}
            RETURN DISTINCT {
                _key: v._key,
                id: v._id,
                nombre: v.nombre,
                tipo: v.tipo,
                subtipo: v.subtipo,
                metricas: v.metricas
            }
        )

    LET links = (
        FOR v, e, p IN 1..@deep ANY @node GRAPH "grafo"
            PRUNE v.nombre == 'DEFENSORIA PUBLICA OFICIAL'
            OPTIONS {bfs: true}
            RETURN DISTINCT {
                source: e._from,
                target: e._to,
                tipo: e.tipo
            }
        )

    return {nodes, links}
    """

    query2 = """
    LET nodes = (
        FOR v, e, p IN 0..@deep ANY @node GRAPH "grafo"
            OPTIONS {bfs: true}
            RETURN DISTINCT {
                _key: v._key,
                id: v._id,
                nombre: v.nombre,
                tipo: v.tipo,
                subtipo: v.subtipo,
                metricas: v.metricas
            }
        )

    LET links = (
        FOR v, e, p IN 1..@deep ANY @node GRAPH "grafo"
            OPTIONS {bfs: true}
            RETURN DISTINCT {
                source: e._from,
                target: e._to,
                tipo: e.tipo
            }
        )

    return {nodes, links}
    """

    if parameters['node'] == 'nodos_entidades/DEFENSORIA_PUBLICA_OFICIAL':
        query = query2
    else:
        query = query1

    bind_vars = {
        'node': parameters['node'],
        'deep': parameters['profundidad']
    }

    data = arangoDB.aql.execute(query, bind_vars=bind_vars)
    results = [r for r in data][0]
    results['nodes'] = [node for node in results['nodes'] if node['id']]
    results['links'] = [
        link for link in results['links']
        if 'nodos_magistrados/SIN_DATO' not in [link['source'], link['target']]
    ]

    return {'grafo': results,
            'execution_time': data.statistics()['execution_time']}
