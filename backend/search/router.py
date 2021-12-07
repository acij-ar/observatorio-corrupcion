from flask_restful import Resource
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource

from plugins import cache
from session import arangoDB
from search import schemas


class Search(MethodResource, Resource):
    @doc(description='Buscar nodos por nombre', tags=['Buscar'])
    @use_kwargs(schemas.Query, location="query")
    @marshal_with(schemas.Search)
    @cache.cached(query_string=True)
    def get(self, q, limit=10):
        return query_search_fulltext(q, limit)



def query_search_fulltext(q: str, limit: int):
    """
    Use ArangoDB Fulltext to search on nodos_entidades and
    nodos_magistrados by name.
    """
    query = """
    LET entidades = (
        FOR d IN FULLTEXT("nodos_entidades", "nombre", @words)
            SORT d.metricas.degree DESC
            LIMIT 50
            RETURN d
        )

    LET magistrados = (
        FOR d IN FULLTEXT("nodos_magistrados", "nombre", @words)
            SORT d.metricas.degree DESC
            LIMIT 50
            RETURN d
        )

    LET causas = (
        FOR d IN FULLTEXT("nodos_causas", "nombre", @words)
            SORT d.metricas.degree DESC
            LIMIT 10
            RETURN d
        )

    FOR d IN APPEND(APPEND(causas, entidades), magistrados)
        SORT d.metricas.degree DESC
        LIMIT @limit_offset
        RETURN { nombre: d.nombre, key: d._key, degree: d.metricas.degree, tipo: d.tipo, sub_tipo: d.sub_tipo }
    """

    bind_vars = {
        'words': q,
        'limit_offset': limit
    }

    data = arangoDB.aql.execute(query, bind_vars=bind_vars)

    results = [r for r in data]
    return {'results': results,
            'execution_time': data.statistics()['execution_time']}
