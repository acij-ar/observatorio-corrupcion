from flask_restful import Resource, reqparse, abort

from session import arangoDB


# Graph query parameters parser
graph_parser = reqparse.RequestParser()
graph_parser.add_argument(
    'profundidad', type=int, required=False, default=2
)


class Graph(Resource):
    """

    """
    # Valid collections
    collections = [collection['name'] for collection in arangoDB.collections()]

    def get(self, collection, document):
        print(collection, self.collections)

        # Check if the collection is valid
        if collection not in self.collections:
            abort(404, message=f'La coleccion "{collection}" no existe')

        args = graph_parser.parse_args()
        args['node'] = collection + '/' + document.replace(' ', '_')
        result = query_graph(args)

        # Check if the node name is valid
        if not result['grafo']['nodes']:
            abort(404, message=f'El nodo "{document}" no existe')

        return result


def query_graph(parameters):
    """

    """
    query1 = """
    LET nodes = (
        FOR v, e, p IN 0..@deep ANY @node GRAPH "grafo"
            PRUNE v.nombre == 'DEFENSORIA PUBLICA OFICIAL'
            OPTIONS {bfs: true}
            RETURN DISTINCT v
        )

    LET links = (
        FOR v, e, p IN 1..@deep ANY @node GRAPH "grafo"
            PRUNE v.nombre == 'DEFENSORIA PUBLICA OFICIAL'
            OPTIONS {bfs: true}
            RETURN DISTINCT e
        )

    return {nodes, links}
    """

    query2 = """
    LET nodes = (
        FOR v, e, p IN 0..@deep ANY @node GRAPH "grafo"
            OPTIONS {bfs: true}
            RETURN DISTINCT v
        )

    LET links = (
        FOR v, e, p IN 1..@deep ANY @node GRAPH "grafo"
            OPTIONS {bfs: true}
            RETURN DISTINCT e
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

    nodes = [node for node in results['nodes'] if node]
    links = [link for link in results['links'] if link]

    # Only return the necesary data
    resultado_nodes = []
    for node in nodes:
        id = node['_id']
        print(id)
        nombre=""
        tipo=""
        subtipo=""
        metricas=""
        if 'nombre' in node:
            nombre=node['nombre']
        if 'tipo' in node:
            tipo=node['tipo']
        if 'subtipo' in node:
            subtipo=node['subtipo']
        if 'metricas' in node:
            metricas=node['metricas']
        if nombre != "":
            resultado_nodes.append({'id': id, 'nombre': nombre,'tipo': tipo, 'subtipo': subtipo,'metricas': metricas})        

    links = [{'source': link['_from'], 'target': link['_to'],
              'tipo': link['tipo']} for link in links]

    results = {
        'nodes': nodes,
        'links': links
    }

    return {'grafo': results,
            'execution_time': data.statistics()['execution_time']}
