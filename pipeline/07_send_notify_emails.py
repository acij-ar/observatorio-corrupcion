from pathlib import Path
from datetime import date, datetime

import pandas as pd

from utils import send_email
from config import settings


attachments = [p for p in Path("data/email").glob("*csv")]

crimes_text = ""
path = Path(settings.BASE_DIR) / "email/delitos_a_fixear.csv"
if path in attachments:
    df = pd.read_csv(path)
    crimes_text = f"""
    <li>
        {len(df._delito.unique())} delitos que no tenemos en nuestro
        <a href="https://docs.google.com/spreadsheets/d/1fLi0PY5Zs08dPFJKH-gdjHV7QIG37m5p/edit#gid=47458294">excel</a>.
        Te adjunto el csv <i>{path.name}</i> para que los agregues.
    </li>
"""

radications_text = ""
path = Path(settings.BASE_DIR) / "email/salas_a_fixear.csv"
if path in attachments:
    df = pd.read_csv(path)
    radications_text = f"""
    <li>
        {len(df.sala.unique())} salas que no tenemos en nuestro
        <a href="https://docs.google.com/spreadsheets/d/18hVdsxsQaxdbz7rfY3aFr3kVHKq38lLq/edit#gid=1333148305">excel</a>.
        Te adjunto el csv <i>{path.name}</i> para que los agregues.
    </li>
"""

stats_text = ""
nodes = [
    {"path": "db/nodos_causas.json", "text": "causas"},
    {"path": "db/nodos_entidades.json", "text": "entidades"},
    {"path": "db/nodos_magistrados.json", "text": "magistrados"},
]
for node in nodes:
    df = pd.read_json(Path(settings.BASE_DIR) / node["path"], lines=True)
    stats_text += f"<li>{len(df._key.unique())} {node['text']} únicos</li>"

stats_text += f"<li>{len(list((Path(settings.BASE_DIR) / 'PDFs').glob('*.pdf')))} PDF de resoluciones procesados</li>"

df = pd.read_json(Path(settings.BASE_DIR) / "db/nodos_entidades.json", lines=True)
group = df.groupby(['tipo', 'sub_tipo']).size()
entities_stats = group.reset_index(name="cantidad").to_html(index=False)

body = f"""
<html>
  <head>
    <style>
      * {{
        box-sizing: border-box;
      }}

      .content {{
        padding: 20px;
        background-color: #ffffff;
        border-radius: 0 0 3px 3px;
        border: 1px solid #e9e9e9;
        border-top: none;
      }}

      .content > a {{
        color: #348eda !important;
      }}

      .footer {{
        margin-top: 20px;
        font-size: 12px;
        text-align: center;
        font-size: 24px;
      }}
    </style>
  </head>
  <body>
    <div class="content">
        <p>Hola! Soy el Bot del Observatorio de Corrupción.</p>

        <p>Scrapie el CIJ y encontré los siguientes problemas:<p>
        <ul>
            {crimes_text}
            {radications_text}
        </ul>

        <p>El <strong>Observatorio</strong> en algunos números:</p>
        <ul>{stats_text}</ul>

        <p>Según tipo de entidad<p>
        {entities_stats}

        <p>Por fa, no me contestes. Esto es lo único que mi creador me enseñó a decir :(<br>
        Cualquier cosa, ponete en contacto con Él.</p>
    </div>
    <div class="footer">
        <p>Que los datos te acompañen.</p>
    </div>
  </body>
</html>
"""

send_email(
  to_=settings.BOT_EMAILS_TO_NOTIFY,
  subject=f"Estadísticas del Observatorio ({datetime.now().strftime('%d-%m-%Y')})",
  html=body,
  attachments=attachments
)
