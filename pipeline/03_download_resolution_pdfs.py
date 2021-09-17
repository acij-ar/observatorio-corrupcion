import asyncio
import subprocess
import collections
from typing import List
from pathlib import Path
from string import ascii_letters, digits

import pandas as pd
from tqdm import tqdm

from config import settings
from utils import logging, download_multi_files, DowloadFile


def find_resolution(row) -> str:
    filepath: Path = settings.BASE_DIR / "PDFs" / row.pdf_nombre
    letters = [l for l in ascii_letters + digits]
    footer_lines = [
        'Poder Judicial de la Nación',
        'CAMARA ',
        'Fecha de firma:',
        'Alta en sistema:',
        'Firmado por:',
        'Firmado(ante mi) por:',
        '#',
        'Y VISTOS Y',
        row.expediente,
        'Año del Bicentenario de la Declaración de la Independencia Nacional']

    # No se por que pero un pdf esta vacio. Lo ignoro
    if filepath.stat().st_size == 0:
        return ''

    try:
        with open(filepath.with_suffix(".txt")) as file:
            lines = [line.replace('\n', '') for line in file.readlines()]
    except:
        print(f"Error con el archivo: {row.pdf_nombre}")
        return ''

    # Remove the PDF header
    for index, line in enumerate(lines):
        if '///nos Aires,' in line:
            lines = lines[index + 1:]
            break
        if '///Buenos Aires' in line:
            lines = lines[index + 1:]
            break

    # Remove the PDF end
    for index, line in enumerate(lines):
        if 'Regístrese' in line:
            lines = lines[:index]
            break

    # Remove white lines
    lines = [l for l in lines if ' '.join(l.split()) != '']
    lines = [l for l in lines if not ' '.join(l.split()).startswith('#')]

    pages_break = [
        i
        for i, l in enumerate(lines)
        if ' '.join(l.split()) if l.startswith('Fecha de firma')
    ]
    pages_break = [0] + pages_break + [len(lines)]
    pages = [[i, j] for i, j in zip(pages_break[:-1], pages_break[1:])]

    # Elimino los espacios en blanco
    for i, page in enumerate(pages):
        # Calculo el promedio de espacios en blanco
        white_spaces = []

        for line in lines[page[0]: page[1]]:
            spaces = [line.find(l) for l in letters if line.find(l) != -1]
            if not spaces:
                white_spaces.append(1000)
            else:
                white_spaces.append(min(spaces))

        # Most common white spaces
        counter = collections.Counter(white_spaces)
        most_common = counter.most_common()[0][0]

        new_lines = []
        for line in lines[page[0]: page[1]]:
            is_footer = any(
                [
                    ' '.join(line.split()).startswith(footer)
                    for footer in footer_lines
                ]
            )
            if not is_footer:
                new_lines.append(line[most_common:])
            else:
                new_lines.append(line)

        lines[page[0]: page[1]] = new_lines

    # Elimino las lineas que son parte del footer
    lines = [
        l
        for l in lines
        if not any([' '.join(l.split()).startswith(s) for s in (footer_lines)])
    ]

    # Armo los parrafos
    paragraphs = []
    p = ''
    for i, line in enumerate(lines):
        if line and line[0] == ' ':
            paragraphs.append(p)
            p = line
        else:
            p = p + ' ' + line
    paragraphs.append(p)

    # Remove white spaces
    paragraphs = [' '.join(p.split()) for p in paragraphs]

    # Termina de 'ASÍ SE RESUELVE'
    resolution = [p for p in paragraphs if 'ASÍ SE' in p or 'ASI SE' in p]
    if resolution:
        return resolution[0]

    # El caso de RSULEVE: y tomo el siguiente parrafo
    # after_resolution = ['RESUELVE', 'RESUELVO', 'RESOLVEMOS']
    resolution = [i + 1 for i, p in enumerate(paragraphs) if 'RES' in p]
    if resolution:
        try:
            return paragraphs[resolution[0]]
        except:
            return paragraphs[resolution[0] - 1]

    return paragraphs[-1]


def find_signatures(pdf_name: str) -> List[List[str]]:
    filepath: Path = settings.BASE_DIR / "PDFs" / pdf_name

    if filepath.stat().st_size == 0:
        return []

    with open(filepath.with_suffix(".txt")) as file:
        firms: List[str] = list(
            set(
                [
                    line
                    for line in file.readlines()
                    if line.startswith('Firmado')
                ]
            )
        )

        # Get the person name and the job
        firms = [firm.split(':')[1] for firm in firms]
        names = [firm.split(',')[0] for firm in firms]
        jobs = [firm.split(',')[1] if ',' in firm else '' for firm in firms]

        names = [' '.join(name.split()).upper() for name in names]
        jobs = [' '.join(job.split()).upper() for job in jobs]

        # Some replaces
        jobs = [
            job.replace(
                'CAMARA', 'CÁMARA'
            ).replace(
                'SECRETARIA', 'SECRETARIO'
            ).replace(
                'JUEZA', 'JUEZ'
            )
            for job in jobs
        ]

        if not jobs:
            names = ['']
            jobs = ['']

        return [
            [pdf_name, names[i], jobs[i]]
            for i in range(len(jobs))
        ]


# Init logger
tqdm.pandas()
logger = logging.getLogger(__name__)

df_resolutions = pd.read_csv(settings.BASE_DIR / "cij/resoluciones.csv")

# Download news PDFs
resolutions: List[DowloadFile] = [
    {
        "url": row.pdf_url,
        "filepath": settings.BASE_DIR / "PDFs/" / row.pdf_nombre,
    }
    for i, row in df_resolutions.iterrows()
]
resolutions = [file for file in resolutions if not file["filepath"].is_file()]
logger.info(f"PDFs: bajando {len(df_resolutions)} nuevos archivos")
asyncio.run(download_multi_files(resolutions))

logger.info("PDFs: convertiendolos a txt")
resolutions = [
    file
    for file in resolutions
    if not file["filepath"].with_suffix(".txt").is_file()
]
for row in tqdm(resolutions, total=len(resolutions)):
    if row["filepath"].stat().st_size == 0:
        continue

    command = f"pdftotext -layout -enc UTF-8 {row['filepath']}"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        logger.error(f"Error convertiendo {row.pdf_nombre}: {error}")

logger.info('PDFs: extrayendo resoluciones')
df_resolutions['resuelve_texto'] = df_resolutions.progress_apply(
    find_resolution, axis=1
)
df_resolutions.to_csv(settings.BASE_DIR / "cij/resoluciones.csv", index=False)

logger.info('PDFs: Extrayendo firmas')
signatures = df_resolutions.pdf_nombre.progress_apply(find_signatures)
signatures = [item for sublist in signatures for item in sublist]
signatures = pd.DataFrame(signatures, columns=["pdf_nombre", "firma", "cargo"])
signatures.to_csv(settings.BASE_DIR / "cij/resoluciones_firma.csv", index=False)
