from flask_cors import CORS
from flask_restful import Api
from flask_caching import Cache

cache = Cache()
cors = CORS()
api = Api()
