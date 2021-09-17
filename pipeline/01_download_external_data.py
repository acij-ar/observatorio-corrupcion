import asyncio
from typing import List, TypedDict

import httpx
import pandas as pd
from tqdm import tqdm
from pydantic import HttpUrl
from bs4 import BeautifulSoup

from config import settings
from utils import logging, clear_string, download_multi_files, DowloadFile


class JusticiapediaEntity(TypedDict):
    nombre: str
    tipo: str
    url: HttpUrl


async def dowload_justiciapedia_entities(
    to: int,
    section_en: str,
    section_es: str,
) -> List[JusticiapediaEntity]:
    rows: List[JusticiapediaEntity] = []
    pages: List[str] = [""] + [f"page/{i}" for i in range(2, to)]

    async with httpx.AsyncClient() as client:
        for page in tqdm(pages, total=len(pages)):
            response = await client.get(f"{justiciapedia_url}/{section_en}/{page}")

            soup = BeautifulSoup(response.text, 'html.parser')
            divs = soup.find('div', {'class': 'profile-table'}).find_all(
                'div', {'class': 'pure-g'}
            )

            for div in divs:
                rows.append({
                    "nombre": div.find(
                        'p', {'class', 'profile-name'}
                    ).text.split('\n')[0],
                    "typo": section_es,
                    "url": div.find('a').attrs['href']
                })

        return rows


async def dowload_justiciapedia_bio(urls: List[HttpUrl]) -> List[str]:
    rows: List[str] = []
    async with httpx.AsyncClient() as client:
        for url in tqdm(urls, total=len(urls)):
            response = await client.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            bio = soup.find('section', {'class': 'profile-excerpt'}).text

            if "Lo sentimos, no hay reseña para este perfil" in bio:
                bio = ""
            rows.append(bio.replace("\n", ""))

        return rows


justiciapedia_url: HttpUrl = 'https://chequeado.com/justiciapedia'
spreadsheets: List[DowloadFile] = [
    {
        "url": "https://docs.google.com/spreadsheets/d/1FM_cId2ZaBYo7jlMpBw8OD5-2eI5ZL2lFvChv-E4MsM/export?format=csv&id=1FM_cId2ZaBYo7jlMpBw8OD5-2eI5ZL2lFvChv-E4MsM&gid=0",
        "filepath": settings.BASE_DIR / "external/correcion_involucrados.csv",
    },
    {
        "url": "https://docs.google.com/spreadsheets/d/19VBXgddyN72XJoULK4PCWOiFNqxj_0kOVOSzyEzOlWk/export?format=csv&id=19VBXgddyN72XJoULK4PCWOiFNqxj_0kOVOSzyEzOlWk&gid=0",
        "filepath": settings.BASE_DIR / "external/correcion_delitos.csv",
    },
    {
        "url": "https://docs.google.com/spreadsheets/d/1i5H-T0IL-3uc7bx2fQ1WV1-OWzyU_764mCDPTc95YYw/export?format=csv&id=1i5H-T0IL-3uc7bx2fQ1WV1-OWzyU_764mCDPTc95YYw&gid=0",
        "filepath": settings.BASE_DIR / "external/correcion_salas.csv",
    },
    {
        "url": "https://docs.google.com/spreadsheets/d/1nYx4zme5DhrX3pTZyw6pHY-devYvAXn_ItW5cpBSJ-I/export?format=csv&id=1nYx4zme5DhrX3pTZyw6pHY-devYvAXn_ItW5cpBSJ-I&gid=0",
        "filepath": settings.BASE_DIR / "external/organismos_estatales.csv",
    },
    {
        "url": "https://docs.google.com/spreadsheets/d/1JbTQdyfbdMilyOBYwAYSk1HFgjr-hNv8jVCX0kvksec/export?format=csv&id=1JbTQdyfbdMilyOBYwAYSk1HFgjr-hNv8jVCX0kvksec&gid=0",
        "filepath": settings.BASE_DIR / "external/descripcion_entidades.csv",
    },
    {
        "url": "https://docs.google.com/spreadsheets/d/1XR2KTajw2FwtUdMFfqZMx0mo5Q2gMyK2WbniLVONiyM/export?format=csv&id=1XR2KTajw2FwtUdMFfqZMx0mo5Q2gMyK2WbniLVONiyM&gid=1021408497",
        "filepath": settings.BASE_DIR / "external/descripcion_causas.csv",
    },
    {
        "url": "https://docs.google.com/spreadsheets/d/1GjP33D5CUX6W-hUzRaiXVsHuk8b_Z8FhIuRiE_4CsV8/export?format=csv&id=1GjP33D5CUX6W-hUzRaiXVsHuk8b_Z8FhIuRiE_4CsV8&gid=534542697",
        "filepath": settings.BASE_DIR / "external/magistrados_federales.csv",
    },
    {
        "url": "https://cdn.buenosaires.gob.ar/datosabiertos/datasets/nombres-permitidos/nombres-permitidos.csv",
        "filepath": settings.BASE_DIR / "external/nombres_permitidos.csv",
    }
]

# Init loggers
tqdm.pandas()
logger = logging.getLogger(__name__)

logger.info(f"Spreadsheet: bajando {len(spreadsheets)} archivos")
asyncio.run(download_multi_files(spreadsheets))

logger.info("Justiciapedia: bajando fiscales")
rows = asyncio.run(dowload_justiciapedia_entities(8, "prosecutors", "fiscal"))
df_prosecutors = pd.DataFrame(rows)

logger.info("Justiciapedia: bajando jueces")
rows = asyncio.run(dowload_justiciapedia_entities(15, "judges", "juez"))
df_judges = pd.DataFrame(rows)

logger.info("Justiciapedia: bajando las bios")
df = pd.concat([df_prosecutors, df_judges])
df = df.drop_duplicates()
df["bios"] = asyncio.run(dowload_justiciapedia_bio(df.url.to_list()))
df.to_csv(settings.BASE_DIR / "external/justiciapedia.csv", index=False)

# Clear some CSV
df_magistrados = pd.read_csv(
    settings.BASE_DIR / "external/magistrados_federales.csv"
).fillna("")
for col in ['camara', 'organo_tipo', 'organo_nombre', 'magistrado_nombre']:
    df_magistrados[col] = df_magistrados[col].apply(clear_string)

df_magistrados.organo_nombre = df_magistrados.organo_nombre.apply(
    lambda ele: ' '.join(ele.split())
)
# No me sirve esta aclaracion
t1 = ' (FISCALÍA CON COMPETENCIA ELECTORAL, ACTÚA TAMBIÉN ANTE LA CNE)'
df_magistrados.organo_nombre = df_magistrados.organo_nombre.apply(
    lambda x: x.replace(t1, '')
)
df_magistrados.to_csv(
    settings.BASE_DIR / "external/magistrados_federales.csv", index=False
)

df_valid_names = pd.read_csv(
    settings.BASE_DIR / 'external/nombres_permitidos.csv', delimiter=';',
)
df_valid_names = df_valid_names[df_valid_names['SEXO'] != 'A']
df_valid_names = df_valid_names[['NOMBRE', 'SEXO']]
df_valid_names.columns = ["name", "gender"]
df_valid_names.gender = df_valid_names.gender.replace('M', -1).replace('F', 1)
df_valid_names.to_csv(
    settings.BASE_DIR / 'external/nombres_permitidos.csv', index=False
)

# Clear scraped data
csvs = [
    "causas.csv",
    "delitos.csv",
    "implicados.csv",
    "radicaciones_del_expediente.csv",
    "resoluciones.csv",
]
for csv in csvs:
    df = pd.read_csv(settings.BASE_DIR / f"scraper/{csv}")
    df = df.drop_duplicates()
    df.to_csv(
        settings.BASE_DIR / f"cij/{csv}", index=False
    )
