from arango import ArangoClient

from config import settings


# Connect to the DB
client = ArangoClient(hosts=settings.ARANGO_HOST)
arangoDB = client.db(
    settings.ARANGO_DB,
    username=settings.ARANGO_USERNAME,
    password=settings.ARANGO_PASSWORD,
)
