from typing import TypedDict, List, Dict

import httpx
import pandas as pd

from config import settings
from utils import logging


class ArangoColection(TypedDict):
    name: str
    type: int


collections_nodes: List[ArangoColection] = [
    {'name': 'nodos_causas', 'type': 2},
    {'name': 'nodos_magistrados', 'type': 2},
    {'name': 'nodos_entidades', 'type': 2},
]

collections_edges: List[ArangoColection] = [
    {'name': 'relacion_magistrados_casos', 'type': 3},
    {'name': 'relacion_personas_casos', 'type': 3},
    {'name': 'relacion_abogados_personas', 'type': 3},
]

collections: List[ArangoColection] = collections_nodes + collections_edges

graph = {
    'name': 'grafo',
    'edgeDefinitions': [
        {
            'collection': 'relacion_magistrados_casos',
            'from': ['nodos_magistrados'],
            'to': ['nodos_causas']
        },
        {
            'collection': 'relacion_personas_casos',
            'from': ['nodos_entidades'],
            'to': ['nodos_causas']
        },
        {
            'collection': 'relacion_abogados_personas',
            'from': ['nodos_entidades'],
            'to': ['nodos_entidades']
        }
    ]
}

auth = {
  "username": settings.ARANGO_USERNAME,
  "password": settings.ARANGO_PASSWORD,
}

# Init loggers
logger = logging.getLogger(__name__)

logger.info("Auth arango user")
response = httpx.post(f"{settings.ARANGO_HOST}/_open/auth", json=auth)
if response.status_code != 200:
    logger.error("Auth invalida")
    exit()
headers = {"Authorization": f"bearer {response.json()['jwt']}"}

with httpx.Client(headers=headers, timeout=None) as client:
    arango_api_url = f"{settings.ARANGO_HOST}/_db/{settings.ARANGO_DB}/_api"

    # Create db if not exist
    dbs = client.get(f"{settings.ARANGO_HOST}/_api/database").json()["result"]
    if settings.ARANGO_DB not in dbs:
        logger.info("Creating db")
        response = client.post(
            f"{settings.ARANGO_HOST}/_api/database",
            json={"name": settings.ARANGO_DB}
        ).json()
        if response["error"]:
            logger.warning(response)

    # Delete all the relations
    for collection in collections_edges:
        logger.info(f"Deleting collection {collection['name']}")
        response = client.delete(
            f"{arango_api_url}/collection/{collection['name']}"
        ).json()
        if response["error"]:
            logger.warning(response)

    # Create collections if not exist
    results: List[Dict] = client.get(
        f"{arango_api_url}/collection"
    ).json()["result"]
    db_collections: List[str] = [
        collection["name"]
        for collection in results
    ]
    new_collections = [
        collection
        for collection in collections
        if collection["name"] not in db_collections
    ]
    for collection in new_collections:
        logger.info(f"Creating collection {collection['name']}")
        response = client.post(
            f"{arango_api_url}/collection", json=collection
        ).json()
        if response["error"]:
            logger.warning(response)

    # Load data
    for collection in collections:
        logger.info(f"Loading {collection['name']} data")
        df = pd.read_json(
            f"{settings.BASE_DIR}/db/{collection['name']}.json",
            lines=True
        )
        data = df.to_dict(orient="records")
        params = {
            "collection": collection["name"],
            "type": "list",
            "details": "true",
            "onDuplicate": "replace",
        }
        response = client.post(
            f"{arango_api_url}/import",
            params=params,
            json=data,
        ).json()
        logger.info(response)

    # Create full-text search
    for collection in collections_nodes:
        logger.info(f"Creating full-text search for {collection['name']}")
        response = client.post(
            f"{arango_api_url}/index",
            params={"collection": collection["name"]},
            json={"type": "fulltext", "fields": ["nombre"]}
        ).json()
        if response["error"]:
            logger.warning(response)

    graphs: List[str] = client.get(f"{arango_api_url}/gharial").json()["graphs"]
    graphs: List[str] = [graph["name"] for graph in graphs]
    if graph["name"] not in graphs:
        logger.info("Creating the graph")
        response = client.post(
            f"{arango_api_url}/gharial", json=graph
        ).json()
        if response["error"]:
            logger.warning(response)

    # Calculate the metris for each node
    query = """
FOR node in @@doc
    LET outdegree = LENGTH(FOR v IN 1..1 OUTBOUND node GRAPH 'grafo' RETURN 1)
    LET indegree = LENGTH(FOR v IN 1..1 INBOUND node GRAPH 'grafo' RETURN 1)

    UPDATE node WITH {
        metricas: {'outdegree': outdegree, 'indegree': indegree, 'degree': outdegree + indegree}
    } IN @@doc
"""
    for collection in collections_nodes:
        logger.info(f"Updating metric for {collection['name']}")
        data = {
            'query': query,
            'bindVars': {'@doc': collection['name']}
        }
        response = client.post(f"{arango_api_url}/cursor", json=data).json()
        if response["error"]:
            logger.warning(response)

    logger.info("Updating entities nodes relations")
    query = """
FOR node in nodos_entidades
    LET denunciante = LENGTH(FOR v, e IN 1..1 OUTBOUND node GRAPH 'grafo' FILTER e.tipo == 'denunciante' RETURN 1)
    LET querellante = LENGTH(FOR v, e IN 1..1 OUTBOUND node GRAPH 'grafo' FILTER e.tipo == 'querellante' RETURN 1)
    LET sobreseido  = LENGTH(FOR v, e IN 1..1 OUTBOUND node GRAPH 'grafo' FILTER e.tipo == 'sobreseido'  RETURN 1)
    LET letrado     = LENGTH(FOR v, e IN 1..1 OUTBOUND node GRAPH 'grafo' FILTER e.tipo == 'letrado'     RETURN 1)
    LET imputado    = LENGTH(FOR v, e IN 1..1 OUTBOUND node GRAPH 'grafo' FILTER e.tipo == 'imputado'    RETURN 1)
    LET denunciado  = LENGTH(FOR v, e IN 1..1 OUTBOUND node GRAPH 'grafo' FILTER e.tipo == 'denunciado'  RETURN 1)
    LET procesado   = LENGTH(FOR v, e IN 1..1 OUTBOUND node GRAPH 'grafo' FILTER e.tipo == 'procesado'   RETURN 1)
    LET demandado   = LENGTH(FOR v, e IN 1..1 OUTBOUND node GRAPH 'grafo' FILTER e.tipo == 'demandado'   RETURN 1)

    UPDATE node WITH {
        relaciones: {
            'denunciante': denunciante,
            'querellante': querellante,
            'sobreseido': sobreseido,
            'letrado': letrado,
            'imputado': imputado,
            'denunciado': denunciado,
            'procesado': procesado,
            'demandado': demandado,
            'investigado': imputado + denunciado + procesado + demandado
        }
    } IN nodos_entidades
"""
    data = {'query': query}
    response = client.post(f"{arango_api_url}/cursor", json=data).json()
    if response["error"]:
            logger.warning(response)
