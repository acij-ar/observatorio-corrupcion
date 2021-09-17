import re
import sys
import logging
import asyncio
from pathlib import Path
from typing import Union, List, TypedDict

import httpx
import aiofiles
import unidecode
from tqdm import tqdm
from pydantic import HttpUrl


logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
)


class DowloadFile(TypedDict):
    filepath: Union[str, Path]
    url: HttpUrl


async def download_file(
    client:httpx.AsyncClient , filepath: Union[str, Path], url: HttpUrl
):
    async with aiofiles.open(filepath, "wb") as f:
        async with client.stream('GET', url) as r:
            async for chunk in r.aiter_bytes():
                await f.write(chunk)


async def download_multi_files(rows: List[DowloadFile], step: int = 100):
    async with httpx.AsyncClient() as client:
        for i in tqdm(range(0, len(rows), step)):
            tasks = []
            for row in rows[i: i+step]:
                tasks.append(asyncio.ensure_future(
                    download_file(
                        client,
                        row["filepath"],
                        row["url"],
                    )
                ))

            await asyncio.gather(*tasks)


def clear_string(txt: str) -> str:
    txt = re.sub("[^\w\d]+", " ", txt)
    return " ".join(txt.split()).upper()


def generate_key(code: str) -> str:
    code = unidecode.unidecode(code)
    return clear_string(code)

# def generate_key(name: str) -> str:
#     # Generate a valid arangoDB key
#     valid = ascii_letters + digits
#     key = unidecode.unidecode(name)
#     return ''.join([l if l in valid else '_' for l in key])
