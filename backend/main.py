from flask import Flask
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

from plugins import api, cache, cors, docs
from config import settings, AppConfig
from graph.router import Graph
from search.router import Search
from node.router import CasesNode, EntityNode, MagistrateNode
from stats.router import (
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
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='API Observatorio de Corrupción',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/',
})

# Add the routers
api.add_resource(Search, '/v1/buscar')
api.add_resource(Graph, '/v1/grafo/<string:collection>/<string:document>')
api.add_resource(CasesNode, '/v1/nodo/nodos_causas/<string:document>')
api.add_resource(EntityNode, '/v1/nodo/nodos_entidades/<string:document>')
api.add_resource(MagistrateNode, '/v1/nodo/nodos_magistrados/<string:document>')
api.add_resource(TopByRelation, '/v1/estadisticas/top_relacion/<string:metric>')
api.add_resource(CaseByYear, '/v1/estadisticas/casos_por_anio')
api.add_resource(TopJudges, '/v1/estadisticas/jueces')
api.add_resource(TopCrimes, '/v1/estadisticas/delitos')
api.add_resource(Duration, '/v1/estadisticas/duracion')
api.add_resource(OldCases, '/v1/estadisticas/casos_viejos')

# Setup flask plugins
cache.init_app(app)
cors.init_app(app, resources={r"/*": {"origins": "*"}})
api.init_app(app)

docs.init_app(app)
docs.register(Search)
docs.register(CasesNode)
docs.register(EntityNode)
docs.register(MagistrateNode)
docs.register(Graph)

if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=settings.APP_DEBUG,
    )
