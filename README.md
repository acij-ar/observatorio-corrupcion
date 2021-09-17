# Scraper de CIJ

EL scraper del Observatorio de Corrupción del [CIJ](https://www.cij.gob.ar/causas-de-corrupcion.html) se compone de tres procesos:

- **Scrapeado**: Baja todos los datos a multiples archivos csv
- **Normalizado**: En esta etapa se unifica los datos scrapeados y se agregagan datos de otras fuentes.
  - Unificamos los nombres de organismos públicos, involucrados, delitos, etc mediantes múltiples spreadsheets.
  - Unimos con datos externos como las biografías obtenidas de [Justiciapedia](https://chequeado.com/justiciapedia/).
  - Bajamos los PDF de resoluciones de cada causa y nos quedamos con el texto de resolución.
  - Notificamos por email en caso de algún problema.
- **Actualizado de la base de datos**: Actualizamos los datos en ArangoDB que después utiliza el Observatorio

![Flujo general](diagrama.png)

## Setup local

```bash
cp .env.sample .env
# Configuramos las vars en .env
docker-compose build

# La proxima vez solo
./run.sh
```
