from flask import Flask

from plugins import api, cache, cors
from config import settings, AppConfig
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

# Init the app
app = Flask(__name__)
app.config.from_object(AppConfig())

# Add the routers
base_path = '/v1/'
api.add_resource(Search, f'{base_path}/buscar')
api.add_resource(Node, f'{base_path}/nodo/<string:collection>/<string:document>')
api.add_resource(Graph, f'{base_path}/grafo/<string:collection>/<string:document>')
api.add_resource(TopByRelation, f'{base_path}/estadisticas/top_relacion/<string:metric>')
api.add_resource(CaseByYear, f'{base_path}/estadisticas/casos_por_anio')
api.add_resource(TopJudges, f'{base_path}/estadisticas/jueces')
api.add_resource(TopCrimes, f'{base_path}/estadisticas/delitos')
api.add_resource(Duration, f'{base_path}/estadisticas/duracion')
api.add_resource(OldCases, f'{base_path}/estadisticas/casos_viejos')

# Setup flask plugins
cache.init_app(app)
cors.init_app(app, resources={r"/*": {"origins": "*"}})
api.init_app(app)

if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=settings.APP_DEBUG,
    )
