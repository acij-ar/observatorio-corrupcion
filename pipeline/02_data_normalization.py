import re
from typing import List

import Levenshtein
import pandas as pd
from tqdm import tqdm

from config import settings
from utils import logging, clear_string


def unique_names(df_involved: pd.DataFrame) -> List[str]:
    "Get the uniques names of the file implicados.csv"
    names = list(set(df_involved['implicado']).union(set(df_involved['letrado'])))
    names = [name for name in names if name != '']
    names.sort()

    return names


def similar_names(
    names: List[str],
    correct_names: List[str],
    ratio_max: int = 1,
    ratio_min: int = 0.75,
) -> pd.DataFrame:
    # Find similar names using Levenshtein distance
    data = []
    for name in tqdm(names, total=len(names)):
        max_ratio = -1
        most_similar = []

        for name2 in correct_names:
            ratio = Levenshtein.ratio(name, name2)

            if ratio_max > ratio > ratio_min and ratio > max_ratio:
                max_ratio = ratio
                most_similar = [ratio, name, name2]
        if most_similar:
            data.append(most_similar)

    return pd.DataFrame(
        data, columns=['rate', 'name', 'match']
    ).sort_values(by=["rate"], ascending=False)


def replace_names(name: str) -> str:
    "Replaces names using with the most similar using the Levenshtein metric"
    df_filter = names_match[names_match['name'] == name]

    if not df_filter.empty:
        return df_filter.values[0][2]
    else:
        return name


# Init logger
tqdm.pandas()
logger = logging.getLogger(__name__)

# Original csv
df_involved = pd.read_csv(settings.BASE_DIR / 'cij/implicados.csv').fillna('')
df_involved["_letrado"] = df_involved.letrado.copy()
df_involved["_implicado"] = df_involved.implicado.copy()
for col in ["relacion", "implicado", "letrado"]:
    df_involved[col] = df_involved[col].apply(clear_string)

df_correct_names = pd.read_csv(
    settings.BASE_DIR / 'external/correcion_involucrados.csv'
).fillna('')

# Nombres similar en el csv original
names = unique_names(df_involved)
total_names_1 = len(names)
names_match = similar_names(names, names)
names_match.to_csv(settings.BASE_DIR / 'email/match_nombres_1.csv', index=False)
names_match = names_match[names_match['rate'] >= 0.9]
df_involved.letrado = df_involved.letrado.apply(replace_names)
df_involved.implicado = df_involved.implicado.apply(replace_names)

# Nombres similares contra el spreadsheet
names = unique_names(df_involved)
total_names_2 = len(names)
names_match = similar_names(
    names, df_correct_names.nombre_original.unique(), 1.1
)
names_match.to_csv(settings.BASE_DIR / 'email/match_nombres_2.csv', index=False)
names_match = names_match[names_match['rate'] >= 0.85]
df_involved.letrado = df_involved.letrado.apply(replace_names)
df_involved.implicado = df_involved.implicado.apply(replace_names)

# Unique names
names = unique_names(df_involved)
total_names_3 = len(names)
print(total_names_1, total_names_2, total_names_3)

#
data = []
for index, row in df_involved.iterrows():
    if row.implicado in df_correct_names.nombre_original.unique():
        row_c = df_correct_names[
            df_correct_names.nombre_original == row.implicado
        ].iloc[0][1:].tolist()
        # Puede que las ultimas dos columnas esten vacias, asi q las filtro
        row_c = [r for r in row_c if r]

        for name in row_c:
            r = row.tolist()
            r[2] = name
            data.append(r)
    else:
        data.append(row.tolist())

df_involved = pd.DataFrame(data, columns=df_involved.columns)
df_involved.to_csv(settings.BASE_DIR / 'cij/implicados.csv', index=False)

# Crimenes
df_crimes = pd.read_csv(settings.BASE_DIR / 'cij/delitos.csv').fillna('')
df_crimes["_delito"] = df_crimes.delito.copy()
df_crimes.delito = df_crimes.delito.apply(clear_string)
df_crimes = df_crimes[df_crimes.delito != '']

correct_crimes = pd.read_csv(
    settings.BASE_DIR / 'external/correcion_delitos.csv'
).fillna('')
correct_crimes.original = correct_crimes.original.apply(clear_string)

crimes = []
for i, row in tqdm(df_crimes.iterrows(), total=len(df_crimes)):
    df_filter = correct_crimes[
        correct_crimes.original == row.delito
    ]

    if not df_filter.empty:
        crimes.append(df_filter.renombre.tolist()[0])
    else:
        crimes.append('')
df_crimes['delito'] = crimes

df_crimes.to_csv(settings.BASE_DIR / 'cij/delitos.csv', index=False)
df_crimes[df_crimes['delito'] == ''].to_csv(
    settings.BASE_DIR / 'email/delitos_a_fixear.csv', index=False
)

#
def remove_dr_dra(name: str) -> str:
    """
    Elimino el DR y DRA del nombre del fiscal
    """
    name = name.replace('Fiscal ', '')
    if name.startswith('DR '):
        return name[3:]
    elif name.startswith('DRA '):
        return name[4:]
    else:
        return name


def fix_camera(sala):
    change1 = [
        ['1', 'I'],
        ['2', 'II'],
        ['3', 'III'],
        ['4', 'IV'],
        ['5', 'V']
    ]
    change2 = [
        ['VOCALIA 13', 'SALA II'], ['VOCALIA 12', 'SALA II'], ['VOCALIA 11', 'SALA IV'],
        ['VOCALIA 10', 'SALA I'], ['VOCALIA 8', 'SALA III'], ['VOCALIA 7', 'SALA III'],
        ['VOCALIA 6', 'SALA IV'], ['VOCALIA 5', 'SALA I'], ['VOCALIA 4', 'SALA IV'],
        ['VOCALIA 3', 'SALA III'],  ['VOCALIA 2', 'SALA I'], ['VOCALIA 1', 'SALA II'],
        ['SALA 1', 'SALA I'], ['SALA 2', 'SALA II'], ['SALA 3', 'SALA III'], ['SALA 4', 'SALA IV']
    ]
    some_cameras = [
        'CÁMARA NACIONAL DE APELACIONES EN LO CRIMINAL Y CORRECCIONAL FEDERAL',
        'CÁMARA NACIONAL DE APELACIONES EN LO CRIMINAL Y CORRECCIONAL'
    ]

    if sala.startswith('CÁMARA'):
        if '-' not in sala:
            camara = sala
            organo_nombre = ''
        else:
            camara, organo_nombre = sala.split('-')

        camara = ' '.join(camara.split())
        organo_nombre = ' '.join(organo_nombre.split())

        if camara in some_cameras:
            for old, new in change1:
                organo_nombre = organo_nombre.replace(old, new)

        if camara == 'CÁMARA FEDERAL DE CASACIÓN PENAL':
            for old, new in change2:
                organo_nombre = organo_nombre.replace(old, new)

        return camara + ' - ' + organo_nombre
    return sala


def fix_fiscalia(fiscalia: str) -> str:
    for key in ['.', '_', '°']:
        fiscalia = fiscalia.replace(key, ' ')

    fiscalia = ' '.join(fiscalia.split())
    fiscalia = fiscalia.replace('FED ', 'FEDERAL ')
    fiscalia = fiscalia.replace('NAC ', 'NACIONAL ')
    fiscalia = fiscalia.replace('CRIM Y CORR ', 'CRIMINAL Y CORRECCIONAL ')

    pattern = 'FISCALIA NACIONAL EN LO CRIMINAL Y CORRECCIONAL FEDERAL N ([0-9]+)'
    matchs = re.match(pattern, fiscalia)
    if matchs:
        num = matchs.groups()[0]
        fiscalia = f'FISCALÍA N° {num} ANTE LOS JUZGADOS NACIONALES DE PRIMERA INSTANCIA EN LO CRIMINAL Y CORRECCIONAL FEDERAL'
        return fiscalia

    pattern = 'FISCALIA NACIONAL EN LO CRIMINAL Y CORRECCIONAL N ([0-9]+)'
    matchs = re.match(pattern, fiscalia)

    if matchs:
        num = matchs.groups()[0]
        fiscalia = f'FISCALÍA Nº {num} ANTE LOS JUZGADOS NACIONALES EN LO CRIMINAL Y CORRECCIONAL'
        return fiscalia
    return fiscalia


def fix_fiscal(row):
    df_filter = df_magistrados[
        df_magistrados.organo_nombre == row.fiscalia
    ]
    if not df_filter.empty:
        return df_filter.iloc[0]['magistrado_nombre']
    else:
        return row['fiscal']


def fix_sala(sala):
    sala = " ".join(sala.split())

    pattern = "FEDERAL (\d+)$"
    matchs = re.search(pattern, sala)
    if matchs:
        num = matchs.groups()[0]
        sala = " ".join(sala.split()[:-1]) + f" N {num}"

    sala = sala.replace(
        "CÁMARA CRIMINAL Y CORRECCIONAL FEDERAL - SALA",
        "CÁMARA NACIONAL DE APELACIONES EN LO CRIMINAL Y CORRECCIONAL FEDERAL - SALA"
    ).replace(
        "JUZGADO CRIMINAL Y CORRECCIONAL FEDERAL N",
        "JUZGADO NACIONAL DE PRIMERA INSTANCIA EN LO CRIMINAL Y CORRECCIONAL FEDERAL N"
    )

    return sala


df_radication = pd.read_csv(
    settings.BASE_DIR / 'cij/radicaciones_del_expediente.csv'
).fillna("")
df_radication.sala = df_radication.sala.str.replace(
    'CAMARA', 'CÁMARA'
).str.replace('CASACION', 'CASACIÓN').str.replace(
    '-$', '', regex=True
).str.replace('.', ' ', regex=False)
df_radication.sala = df_radication.sala.apply(fix_sala)
df_radication.fiscal = df_radication.fiscal.apply(clear_string)
df_radication.fiscal = df_radication.fiscal.apply(remove_dr_dra)
df_radication['sala_c'] = df_radication.sala

correct_cameras = pd.read_csv(
    settings.BASE_DIR / 'external/correcion_salas.csv'
).fillna("")
correct_cameras.columns = [col.lower() for col in correct_cameras.columns]
correct_cameras.nombre = correct_cameras.nombre.apply(clear_string)

df_magistrados = pd.read_csv(
    settings.BASE_DIR / 'external/magistrados_federales.csv'
).fillna("")
for col in ["camara", "organo_tipo", "organo_nombre", "magistrado_nombre"]:
    df_magistrados[col] = df_magistrados[col].apply(clear_string)

#
for index, row in correct_cameras.iterrows():
    df_radication.sala_c = df_radication.sala_c.str.replace(
        row.nombre, row.renombre
    )
df_radication.sala_c = df_radication.sala_c.apply(fix_camera)


data = []
for index, row in df_radication.iterrows():
    organo_tipo = row.sala_c.split()[0]
    line = ['', '', '', '', '', '']

    if organo_tipo == 'TRIBUNAL':
        df_filter = df_magistrados[df_magistrados.organo_nombre == row.sala_c]

        if not df_filter.empty:
            desc = df_filter[
                ['camara', 'organo_tipo', 'organo_nombre']
            ].iloc[0].tolist()
            jueces = df_filter['magistrado_nombre'].tolist()
            line = desc + jueces
    elif organo_tipo == 'JUZGADO':
        df_filter = df_magistrados[df_magistrados.organo_nombre == row.sala_c]
        if not df_filter.empty:
            desc = df_filter[
                ['camara', 'organo_tipo', 'organo_nombre']
            ].iloc[0].tolist()
            jueces = df_filter['magistrado_nombre'].tolist() + ['', '']
            line = desc + jueces
    elif organo_tipo == 'CÁMARA':
        camara, organo_nombre = row.sala_c.split(' - ')
        df_filter = df_magistrados[
            (df_magistrados.camara == camara) &
            (df_magistrados.organo_nombre == organo_nombre)
        ]

        if not df_filter.empty:
            desc = df_filter[
                ['camara', 'organo_tipo', 'organo_nombre']
            ].iloc[0].tolist()
            jueces = df_filter['magistrado_nombre'].tolist()
            line = desc + jueces[:3]

    data.append(line)

df_judges = pd.DataFrame(data, columns=[
    'camara', 'organo_tipo', 'organo_nombre', 'juez_1', 'juez_2', 'juez_3'
])
df_radication = df_radication.drop(columns=['sala_c'])
df_radication = pd.merge(
    df_radication, df_judges, right_index=True, left_index=True
)
df_radication.fiscalia = df_radication.fiscalia.fillna("").apply(fix_fiscalia)
df_radication.fiscal = df_radication.fillna("").apply(fix_fiscal, axis=1)

df_radication.to_csv(
    settings.BASE_DIR / 'cij/radicaciones_del_expediente.csv', index=False
)
df_radication[df_radication.camara == ''].to_csv(
    settings.BASE_DIR / 'email/salas_a_fixear.csv', index=False
)
