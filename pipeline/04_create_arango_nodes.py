import unidecode
import pandas as pd

from config import settings
from utils import logging, generate_key


def calc_type(row):
    # Empresas
    if row.nombre.endswith(' SA'):
        return ['empresa', 'SA']
    elif row.nombre.endswith(' SOCIEDAD ANÓNIMA'):
        return ['empresa', 'SA']
    elif row.nombre.endswith(' SE'):
        return ['empresa', 'SE']
    elif row.nombre.endswith(' SRL'):
        return ['empresa', 'SRL']
    elif row.nombre.endswith(' LTD'):
        return ['empresa', 'LTD']
    elif row.nombre.endswith(' INC'):
        return ['empresa', 'SA']
    elif row.nombre.endswith(' LLC'):
        return ['empresa', 'SRL']
    elif row.nombre.endswith(' CORP') or row.nombre.endswith(' COORP'):
        return ['empresa', '']
    elif row.nombre.endswith(' CORPORATION'):
        return ['empresa', '']
    elif row.nombre.startswith('COOPERATIVA '):
        return ['empresa', 'cooperativa']
    elif row.nombre.startswith('GRUPO '):
        return ['empresa', '']

    # Organismos estatales
    if row.nombre.startswith('JUZGADO '):
        return ['organismo estatal', 'juzgado']
    elif row.nombre.startswith('FISCALIA') or row.nombre.startswith('FISCALÍA'):
        return ['organismo estatal', 'fiscalia']
    elif row.nombre.startswith('MINISTERIO '):
        return ['organismo estatal', 'ministerio']
    elif row.nombre.startswith('SECRETARIA '):
        return ['organismo estatal', 'secretaria']

    df_filter = df_orga[df_orga.nombre == row.nombre]
    if not df_filter.empty:
        return ['organismo estatal', '']

    # ONG
    if row.nombre.startswith('ASOCIACION'):
        return ['ong', 'asociacion civil']
    elif row.nombre.endswith(' ASOCIACION CIVIL'):
        return ['ong', 'asociacion civil']
    elif row.nombre.startswith('FUNDACION') or row.nombre.startswith('FUNDACIÓN'):
        return ['ong', 'fundacion']
    elif row.nombre.endswith(' ONG'):
        return ['ong', '']
    elif row.nombre.startswith('PARTIDO '):
        return ['ong', 'partido politico']

    # Personas
    cnt = 0
    name = unidecode.unidecode(row.nombre)

    for n in name.split():
        df_filter = df_valid_names[df_valid_names.name == n]
        if not df_filter.empty:
            cnt += df_filter.values[0][1]

    if cnt > 0:
        return ['persona', 'mujer']
    elif cnt < 0:
        return ['persona', 'hombre']

    return ['entidad', '']


# Init loggers
logger = logging.getLogger(__name__)

logger.info("Creando los nodos 'Casos'")
df_cases = pd.read_csv(settings.BASE_DIR / 'cij/causas.csv').fillna("")
df_resolutions = pd.read_csv(
    settings.BASE_DIR / 'cij/resoluciones.csv'
).fillna("")
df_radication = pd.read_csv(
    settings.BASE_DIR / 'cij/radicaciones_del_expediente.csv'
).fillna("")
df_crimes = pd.read_csv(
    settings.BASE_DIR / 'cij/delitos.csv'
).fillna("")
df_descriptions = pd.read_csv(
    settings.BASE_DIR / 'external/descripcion_causas.csv'
).fillna("")

# Add description
df_cases = df_cases.join(
    df_descriptions.set_index('expediente'), on='expediente'
)

# Add crimes
crimes = []
for index, row in df_cases.iterrows():
    df_filter = df_crimes[df_crimes.expediente == row.expediente]
    if not df_filter.empty:
        crimes.append(
            [c for c in df_filter.delito.tolist() if c != '']
        )
    else:
        crimes.append([])
df_cases['delitos'] = crimes

# Add resolutions
resolutions = []
for index, row in df_cases.iterrows():
    df_filter = df_resolutions[df_resolutions.expediente == row.expediente]
    df_filter = df_filter.drop(columns='expediente')

    if not df_filter.empty:
        resolutions.append(df_filter.to_dict(orient='records'))
    else:
        resolutions.append([])
df_cases['resoluciones'] = resolutions

# Add radications
radications = []
jueces = []
fiscales = []
for index, row in df_cases.iterrows():
    df_filter = df_radication[df_radication.expediente == row.expediente]
    df_filter = df_filter.drop(columns='expediente')
    df_filter = df_filter.sort_values('fecha', ascending=True)

    if not df_filter.empty:
        radications.append(df_filter.to_dict(orient='records'))
    else:
        radications.append([])

    # Obtengo el juez y fiscal federal
    t = 'JUZGADO NACIONAL DE PRIMERA INSTANCIA EN LO CRIMINAL Y CORRECCIONAL FEDERAL N '
    if not df_filter[df_filter.organo_nombre.str.startswith(t)].empty:
        fiscal = df_filter[df_filter.organo_nombre.str.startswith(t)].iloc[0]['fiscal']
        juez = df_filter[df_filter.organo_nombre.str.startswith(t)].iloc[0]['juez_1']
    else:
        fiscal = 'sin dato'
        juez = 'sin dato'

    jueces.append(juez)
    fiscales.append(fiscal)

df_cases['radicaciones'] = radications
df_cases['juez'] = jueces
df_cases['fiscal'] = fiscales
df_cases['tipo'] = 'expediente judicial'
df_cases['anio_comienzo'] = df_cases.expediente.apply(
    lambda x: int(x.split('/')[-1])
)

df_cases['_key'] = df_cases.expediente.apply(generate_key)
df_cases = df_cases.drop_duplicates(subset=['_key'], keep='first')
df_cases.to_json(
    settings.BASE_DIR / 'db/nodos_causas.json', orient="records", lines=True
)
logger.info(f"{len(df_cases)} nodos 'Casos' creados")

#
logger.info("Creando los nodos 'Magistrados'")
df_magistrados = pd.read_csv(
    settings.BASE_DIR / 'external/magistrados_federales.csv'
).fillna("")
df_magistrados = df_magistrados[df_magistrados.magistrado_nombre != '']

df_magistrados['nombre'] = df_magistrados.magistrado_nombre
df_magistrados['tipo'] = 'magistrado'
df_magistrados['subtipo'] = df_magistrados.cargo_tipo.str.lower()
df_magistrados['_key'] = df_magistrados.nombre.apply(generate_key)
df_magistrados = df_magistrados.drop(columns=['magistrado_nombre'])

df_magistrados = df_magistrados.drop_duplicates(
    subset=['_key'], keep='first'
)
df_magistrados.to_json(
    settings.BASE_DIR / 'db/nodos_magistrados.json', orient="records", lines=True
)
logger.info(f"{len(df_magistrados)} nodos 'Magistrados' creados")

#
logger.info("Creando los nodos 'Entidades'")
df_orga = pd.read_csv(settings.BASE_DIR / 'external/organismos_estatales.csv')
df_valid_names = pd.read_csv(
    settings.BASE_DIR / 'external/nombres_permitidos.csv'
)
df_descriptions = pd.read_csv(
    settings.BASE_DIR / 'external/descripcion_entidades.csv'
)
df_descriptions.foto = df_descriptions.foto + ".jpg"


df_involved = pd.read_csv(settings.BASE_DIR / 'cij/implicados.csv')
names = df_involved.implicado.tolist() + df_involved.letrado.tolist()
df_entities = pd.DataFrame(names, columns=['nombre'])
df_entities = df_entities.dropna()

# Cuento la cantidad de apariciones de cada nombre
df_entities = df_entities.groupby('nombre')['nombre'].count()
df_entities = df_entities.reset_index(name='cardinal')
df_entities = df_entities.sort_values(by='cardinal')

result = df_entities.apply(calc_type, axis=1, result_type='expand')
result.columns = ['tipo', 'sub_tipo']
df_entities = df_entities.join(result)
df_entities = df_entities.reset_index(drop=True)
print(df_entities.groupby(['tipo', 'sub_tipo']).size())

#
valid_names = df_descriptions.nombre_entidad.unique()
bio = [
    df_descriptions[df_descriptions.nombre_entidad == name].biografía.values[0]
    if name in valid_names else ''
    for name in df_entities.nombre
]
photo = [
    df_descriptions[df_descriptions.nombre_entidad == name]['foto'].values[0]
    if name in valid_names else ''
    for name in df_entities.nombre
]
df_entities['bio'] = bio
df_entities['foto'] = photo
df_entities['_key'] = df_entities.nombre.apply(generate_key)

df_entities = df_entities.drop_duplicates(subset=['_key'], keep='first')
df_entities.to_json(
    settings.BASE_DIR / 'db/nodos_entidades.json', orient='records', lines=True
)
logger.info(f"{len(df_entities)} nodos 'Entidades' creados")
