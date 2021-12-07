from flask_cors import CORS
from flask_restful import Api
from flask_caching import Cache
from flask_apispec import FlaskApiSpec

cache = Cache()
cors = CORS()
api = Api()
docs = FlaskApiSpec()
