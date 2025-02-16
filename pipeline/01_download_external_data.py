import asyncio
from typing import List, TypedDict, Optional

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
            profile_table = soup.find('div', {'class': 'profile-table'})
            if not profile_table:
                continue  # Evita errores si no encuentra la tabla

            divs = profile_table.find_all('div', {'class': 'pure-g'})

            for div in divs:
                name_tag = div.find('p', {'class': 'profile-name'})
                name = name_tag.text.split('\n')[0] if name_tag else "Desconocido"

                link_tag = div.find('p', class_='simple-link-wrapper')
                url_tag = link_tag.find('a') if link_tag else None
                url = url_tag.attrs['href'] if url_tag else None

                rows.append({
                    "nombre": name,
                    "typo": section_es,
                    "url": url
                })
        return rows


async def dowload_justiciapedia_bio(urls: List[Optional[str]]) -> List[str]:
    rows = [""] * len(urls)  # Inicializa con el mismo tamaño que urls
    async with httpx.AsyncClient() as client:
        for i, url in tqdm(list(enumerate(urls)), total=len(urls)):  
            if not url:
                continue  # Deja el "" en su lugar si url es None

            try:
                response = await client.get(str(url))
                soup = BeautifulSoup(response.text, 'html.parser')
                bio = soup.find('section', {'class': 'profile-excerpt'})
                bio_text = bio.text if bio else ""

                if "Lo sentimos, no hay reseña para este perfil" in bio_text:
                    bio_text = ""

                rows[i] = bio_text.replace("\n", "")
            except Exception as e:
                print(f"Error con {url}: {e}")

    return rows



justiciapedia_url: HttpUrl = 'https://chequeado.com/justiciapedia'
spreadsheets: List[DowloadFile] = [
    {
        "url": "https://docs.google.com/spreadsheets/d/1QO5-lRxeYyKO7KePZN4Q8FfJqTExNPzO/export?format=csv",
        "filepath": settings.BASE_DIR / "external/correcion_involucrados.csv",
    },
    {
        "url": "https://docs.google.com/spreadsheets/d/1fLi0PY5Zs08dPFJKH-gdjHV7QIG37m5p/export?format=csv",
        "filepath": settings.BASE_DIR / "external/correcion_delitos.csv",
    },
    {
        "url": "https://docs.google.com/spreadsheets/d/18hVdsxsQaxdbz7rfY3aFr3kVHKq38lLq/export?format=csv",
        "filepath": settings.BASE_DIR / "external/correcion_salas.csv",
    },
    {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vTWAFAs842Wh9iM43i2wG7WDL45di_oU21_qSnn4KuYNzvR-w4qI3d003wqbv2YYMxMo4R8DyWBqVGO/pub?output=csv",
        "filepath": settings.BASE_DIR / "external/correccion_magistrados.csv",
    },
    {
        "url": "https://docs.google.com/spreadsheets/d/1CezXWSnZ901HAH4PkQ9h1li05W-pJBKX/export?format=csv",
        "filepath": settings.BASE_DIR / "external/organismos_estatales.csv",
    },
    {
        "url": "https://docs.google.com/spreadsheets/d/14GL2zTRYqSg3qGGFSLtRVN3EY8mxKnk7/export?format=csv",
        "filepath": settings.BASE_DIR / "external/descripcion_entidades.csv",
    },
    {
        "url": "https://docs.google.com/spreadsheets/d/1ir54baPOBn8W9JFPIw2hFaNqNoo-U2xX/export?format=csv",
        "filepath": settings.BASE_DIR / "external/descripcion_causas.csv",
    },
    {
        "url": "https://docs.google.com/spreadsheets/d/1TWdPuCGmcfQDN0TDSm8lUDx2SiGvOFqdCZ7i2zE-THs/export?format=csv",
        "filepath": settings.BASE_DIR / "external/descripcion_magistrados.csv",
    },
    {
        "url": "https://docs.google.com/spreadsheets/d/1eQkYUVQyY9kXaWeG5z9NzPjZ7_jitJv8QDRFhbRGixA/export?format=csv",
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
