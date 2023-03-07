import re
import sys
import logging
import asyncio
import smtplib, ssl
from pathlib import Path
from typing import Union, List, TypedDict
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import httpx
import aiofiles
import unidecode
from tqdm import tqdm
from pydantic import HttpUrl, EmailStr

from config import settings


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
    sslcontext = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    async with httpx.AsyncClient(verify = sslcontext, timeout = 20, headers={"Connection": "close"}) as client:
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
    code = clear_string(code)
    return "_".join(code.split())


def send_email(
    to_: Union[EmailStr, List[EmailStr]],
    subject: str,
    html: str,
    attachments: List[Union[str, Path]] = [],
):
    if isinstance(to_, str):
        to_: List[EmailStr] = [to_]

    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = settings.BOT_EMAIL_USER
    message["To"] = ", ".join(to_)

    body = MIMEText(html, "html")
    message.attach(body)

    for path in attachments:
        part = MIMEBase('application', "octet-stream")
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={Path(path).name}"
        )
        message.attach(part)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(settings.BOT_EMAIL_USER, settings.BOT_EMAIL_PASSWORD)
        server.sendmail(
            settings.BOT_EMAIL_USER, to_, message.as_string()
        )
