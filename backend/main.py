from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from config import settings
from routers.search import Search
from routers.graph import Graph
from routers.node import Node
from routers.stats import (
    TopByRelation,
    TopJudges,
    CaseByYear,
    TopCrimes,
    OldCases,
    Duration,
)

app = Flask(__name__)
app.config.from_mapping(
    APP_NAME = settings.APP_NAME,
    DEBUG = settings.APP_DEBUG,
    THREADS_PER_PAGE = settings.APP_THREADS_PER_PAGE,
    CSRF_ENABLED = settings.APP_CSRF_ENABLED,
    CSRF_SESSION_KEY = settings.APP_CSRF_SESSION_KEY,
    SECRET_KEY = settings.APP_SECRET_KEY,
)

# Setup flask plugins
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)

# Add the routers
base_path = '/v1/'
api.add_resource(Search, base_path + 'buscar')
api.add_resource(Node, base_path + 'nodo/<string:collection>/<string:document>')
api.add_resource(Graph, base_path + 'grafo/<string:collection>/<string:document>')
api.add_resource(TopByRelation, base_path + 'estadisticas/top_relacion/<string:metric>')
api.add_resource(CaseByYear, base_path + 'estadisticas/casos_por_anio')
api.add_resource(TopJudges, base_path + 'estadisticas/jueces')
api.add_resource(TopCrimes, base_path + 'estadisticas/delitos')
api.add_resource(Duration, base_path + 'estadisticas/duracion')
api.add_resource(OldCases, base_path + 'estadisticas/casos_viejos')

# api.add_resource(Search, f'{base_path}/buscar')
# api.add_resource(Node, f'{base_path}/nodo/<string:collection>/<string:document>')
# api.add_resource(Graph, f'{base_path}/grafo/<string:collection>/<string:document>')
# api.add_resource(TopByRelation, f'{base_path}/estadisticas/top_relacion/<string:metric>')
# api.add_resource(CaseByYear, f'{base_path}/estadisticas/casos_por_anio')
# api.add_resource(TopJudges, f'{base_path}/estadisticas/jueces')
# api.add_resource(TopCrimes, f'{base_path}/estadisticas/delitos')
# api.add_resource(Duration, f'{base_path}/estadisticas/duracion')
# api.add_resource(OldCases, f'{base_path}/estadisticas/casos_viejos')

if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
