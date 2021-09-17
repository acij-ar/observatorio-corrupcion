import pandas as pd

from config import settings
from utils import logging, generate_key


# Init loggers
logger = logging.getLogger(__name__)

logger.info("Creado relaciones 'entities2case'")
df_involves = pd.read_csv(
    settings.BASE_DIR / 'cij/implicados.csv'
).fillna('')
df_involves.expediente = df_involves.expediente.apply(generate_key)
df_involves.implicado = df_involves.implicado.apply(generate_key)
df_involves.letrado = df_involves.letrado.apply(generate_key)
df_involves.relacion = df_involves.relacion.str.lower()

rows = [
    {
        "_from": 'nodos_entidades/' + row.implicado,
        "_to": 'nodos_causas/' + row.expediente,
        "_tipo": row.relacion,
    }
    for i, row in df_involves.iterrows()
]
entities2case = pd.DataFrame(rows)
entities2case = entities2case.drop_duplicates()
entities2case = entities2case[entities2case['_from'] != 'nodos_entidades/']
entities2case.to_json(
    settings.BASE_DIR / 'db/relacion_personas_casos.json', orient='records', lines=True
)
logger.info(f"{len(entities2case)} relaciones 'entities2case' creadas")

logger.info("Creado relaciones 'magisters2case'")
df_cases = pd.read_json(settings.BASE_DIR / 'db/nodos_causas.json', lines=True)
df_cases.juez = df_cases.juez.apply(generate_key)
df_cases.fiscal = df_cases.fiscal.apply(generate_key)

rows = [
    {
        "_from": 'nodos_magistrados/' + row.juez,
        "_to": 'nodos_causas/' + row._key,
        "tipo": "juez"
    }
    for i, row in df_cases.iterrows()
] + [
    {
        "_from": 'nodos_magistrados/' + row.fiscal,
        "_to": 'nodos_causas/' + row._key,
        "tipo": "fiscal"
    }
    for i, row in df_cases.iterrows()
]
m2cases = pd.DataFrame(rows)
m2cases = m2cases[m2cases._from != '']
m2cases.to_json(
    settings.BASE_DIR / 'db/relacion_magistrados_casos.json', orient='records', lines=True
)
logger.info(f"{len(m2cases)} relaciones 'magisters2case' creadas")

logger.info("Creado relaciones 'lawyer2person'")
rows = [
    {
        "_from": 'nodos_entidades/' + row.letrado,
        "_to": 'nodos_entidades/' + row.implicado,
        "tipo": "letrado"
    }
    for i, row in df_involves.iterrows()
]
lawyer2person = pd.DataFrame(rows)
lawyer2person = lawyer2person.drop_duplicates()
lawyer2person = lawyer2person[lawyer2person._from != 'nodos_entidades/']
lawyer2person.to_json(
    settings.BASE_DIR / 'db/relacion_abogados_personas.json', orient='records', lines=True
)
logger.info(f"{len(lawyer2person)} relaciones 'lawyer2person' creadas")
