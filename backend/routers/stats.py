import numpy as np
from flask_restful import Resource, reqparse, abort

from session import arangoDB


# Graph query parameters parser
top_parser = reqparse.RequestParser()
top_parser.add_argument(
    'limite', type=int, required=False, default=10
)


class TopByRelation(Resource):
    """

    """
    # Valid metrics
    metrics = ['denunciante', 'querellante', 'sobreseido', 'investigado']

    def get(self, metric):
        args = top_parser.parse_args()
        args['metric'] = metric

        # Check
        if metric not in self.metrics:
            abort(404, message=f'La metrica "{metric}" no es valida. Tiene que ser alguna se las siguentes: {self.metrics}')

        result = query_top_by_relation(args)
        return result


class TopJudges(Resource):
    """

    """
    def get(self):
        """

        """
        result = query_top_judges()
        return result


class TopCrimes(Resource):
    """

    """
    def get(self):
        """

        """
        return 'spam'


class CaseByYear(Resource):
    """

    """
    def get(self):
        """

        """
        result = query_case_by_year()
        return result


class TopCrimes(Resource):
    def get(self):
        return query_crimes()


class OldCases(Resource):
    def get(self):
        return query_old_cases()


class Duration(Resource):
    def get(self):
        return query_duration()


def query_top_by_relation(parameters):
    """

    """
    query = """
    FOR node in nodos_entidades
        SORT node.relaciones[@metric] DESC
        LIMIT @limit
        RETURN { _key: node._key, nombre: node.nombre,
                cantidad: node.relaciones[@metric],
                relaciones: node.relaciones }
    """

    bind_vars = {
        'metric': parameters['metric'],
        'limit': parameters['limite']
    }

    data = arangoDB.aql.execute(query, bind_vars=bind_vars)
    result = [r for r in data]

    return {'resultado': result,
            'execution_time': data.statistics()['execution_time']}


def query_top_judges():
    """

    """
    query = """
    LET judges = UNIQUE(FOR case IN nodos_causas RETURN case.juez)

    FOR judge_name IN judges
        // Total de casos que tiene
        LET t = LENGTH(FOR cases IN nodos_causas
            FILTER cases.juez == judge_name
            RETURN 1)

        // Casos cerrados
        LET c = LENGTH(FOR cases IN nodos_causas
            FILTER cases.terminado == true AND cases.juez == judge_name
            RETURN 1)

        // Casos abiertos
        LET a = LENGTH(FOR cases IN nodos_causas
            FILTER cases.terminado == false AND cases.juez == judge_name
            RETURN 1)

        // A juicio oral
        LET d = LENGTH(FOR cases IN nodos_causas
            // FILTER cases.terminado == true AND cases.estado IN ['ELEVACION A JUICIO ORAL PARCIAL', 'ELEVACION A JUICIO ORAL TOTAL'] AND cases.juez == judge_name
            FILTER cases.estado IN ['ELEVACION A JUICIO ORAL PARCIAL', 'ELEVACION A JUICIO ORAL TOTAL'] AND cases.juez == judge_name
            RETURN 1)

        LET judge = (
            FOR jj IN nodos_magistrados
                FILTER jj.nombre == judge_name
                RETURN jj
        )

        RETURN { juez: {nombre: judge_name, organo_nombre: judge[0].organo_nombre}, total: t, juicio_oral: d, casos_cerrados: c, casos_abiertos: a}
    """
    data = arangoDB.aql.execute(query)
    result = []

    for r in data:
        if r['juez']['nombre'] != 'sin dato':
            s = r['juez']['organo_nombre'].split()
            r['juez']['nombre'] = f"Juzgado Nº {s[-1]} ({r['juez']['nombre']})"
        result.append(r)

    return {'resultado': result,
            'execution_time': data.statistics()['execution_time']}


def query_case_by_year():
    """

    """
    query = """
    LET years = UNIQUE(FOR case IN nodos_causas RETURN case.anio_comienzo)

    FOR year in years
        let d = LENGTH(FOR case in nodos_causas
            FILTER case.anio_comienzo == year
            RETURN 1)
        RETURN { name: year, value: d }
    """

    data = arangoDB.aql.execute(query)
    result = [r for r in data]

    return {'resultado': result,
            'execution_time': data.statistics()['execution_time']}


def query_crimes():
    query = """
    LET crimes = UNIQUE((
            FOR case IN nodos_causas RETURN case.delitos
        )[**])

    LET bins = (FOR crime IN crimes
        let d = LENGTH(FOR case in nodos_causas
            FILTER crime IN case.delitos
            RETURN 1)
        // RETURN {[crime]: d}
        RETURN {crimen: crime, cantidad: d})

    FOR bin IN bins
        SORT bin.cantidad DESC
        LIMIT 20
        RETURN bin
    """
    data = arangoDB.aql.execute(query)
    result = [r for r in data]

    return {'resultado': result,
            'execution_time': data.statistics()['execution_time']}


def query_old_cases():
    query = """
    FOR case IN nodos_causas
        FILTER case.terminado == false
        SORT case.anio_comienzo ASC
        LIMIT 10
        RETURN case
    """
    data = arangoDB.aql.execute(query)
    result = [r for r in data]

    return {'resultado': result,
            'execution_time': data.statistics()['execution_time']}


def query_duration():
    # Causas cerradas
    query = """
    FOR case IN nodos_causas
        FILTER case.terminado == true
        RETURN DATE_YEAR(DATE_NOW()) - case.anio_comienzo
    """
    data = arangoDB.aql.execute(query)
    result = [r for r in data]

    hist, bins = np.histogram(result, bins=[0, 3, 6, 10, 100])
    bins_ter = [
        {'bin': '≤ 3 años', 'value': int(hist[0]), 'p': hist[0]*100/len(result)},
        {'bin': '> 3 a 6 años', 'value': int(hist[1]), 'p': hist[1]*100/len(result)},
        {'bin': '> 6 a 10 años', 'value': int(hist[2]), 'p': hist[2]*100/len(result)},
        {'bin': '> 10 años', 'value': int(hist[3]), 'p': hist[3]*100/len(result)}
    ]

    # Causas abiertas
    query = """
    FOR case IN nodos_causas
        FILTER case.terminado == false
        RETURN DATE_YEAR(DATE_NOW()) - case.anio_comienzo
    """
    data = arangoDB.aql.execute(query)
    result = [r for r in data]

    hist, bins = np.histogram(result, bins=[0, 3, 6, 10, 100])
    bins_ab = [
        {'bin': '≤ 3 años', 'value': int(hist[0]), 'p': hist[0]*100/len(result)},
        {'bin': '> 3 a 6 años', 'value': int(hist[1]), 'p': hist[1]*100/len(result)},
        {'bin': '> 6 a 10 años', 'value': int(hist[2]), 'p': hist[2]*100/len(result)},
        {'bin': '> 10 años', 'value': int(hist[3]), 'p': hist[3]*100/len(result)}
    ]

    bins = {
        'terminadas': bins_ter,
        'abiertas': bins_ab
    }

    return {'resultado': bins,
            'execution_time': data.statistics()['execution_time']}
