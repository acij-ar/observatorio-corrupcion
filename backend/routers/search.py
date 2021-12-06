from flask_restful import Resource, reqparse

from plugins import cache
from session import arangoDB


# Search query parameters parser
search_parser = reqparse.RequestParser()

search_parser.add_argument(
    'q', dest='query', type=str,
    required=True,
    help='Persona/Entidad a buscar'
)

search_parser.add_argument(
    'pagina', dest='page', type=int,
    required=False, default=1,
    help='Pagina de la busqueda (int)'
)

search_parser.add_argument(
    'por_pagina', dest='per_page', type=int,
    required=False, default=10,
    help='Cantidad de resutlados por pagina (int)'
)


class Search(Resource):
    """

    """
    @cache.cached(query_string=True)
    def get(self):
        args = search_parser.parse_args()
        result = query_search_fulltext(args)
        return result


def query_search_fulltext(parameters):
    """
    Use ArangoDB Fulltext to search on nodos_entidades and
    nodos_magistrados by name.
    """
    query = """
    LET entidades = (
        FOR d IN FULLTEXT("nodos_entidades", "nombre_ascii", @words)
            SORT d.metricas.degree DESC
            LIMIT 50
            RETURN d
        )

    LET magistrados = (
        FOR d IN FULLTEXT("nodos_magistrados", "nombre_ascii", @words)
            SORT d.metricas.degree DESC
            LIMIT 50
            RETURN d
        )

    LET causas = (
        FOR d IN FULLTEXT("nodos_causas", "nombre_ascii", @words)
            SORT d.metricas.degree DESC
            LIMIT 10
            RETURN d
        )

    FOR d IN APPEND(APPEND(causas, entidades), magistrados)
        SORT d.metricas.degree DESC
        LIMIT @limit_offset
        // RETURN d
        RETURN { nombre: d.nombre, key: d._key, degree: d.metricas.degree, tipo: d.tipo, sub_tipo: d.sub_tipo }
    """

    bind_vars = {
        'words': parameters['query'],
        'limit_offset': 10
    }

    data = arangoDB.aql.execute(query, bind_vars=bind_vars)

    results = [r for r in data]
    return {'results': results,
            'execution_time': data.statistics()['execution_time']}
