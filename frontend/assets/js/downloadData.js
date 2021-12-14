/*
  Data to CSV
*/

function generateCSV (csvName, header, rows) {
  /*
    Generate a valid csv file given the row and download it.
  */
  let csvContent = "data:text/csv;charset=utf-8,"
      + header.join(",") + "\n"
      + rows.map(r => r.join(",")).join("\n")

  let encodedUri = encodeURI(csvContent)

  // Create an a element and add the csv
  let link = document.createElement("a")
  link.setAttribute("href", encodedUri)
  link.setAttribute("download", csvName)
  document.body.appendChild(link) // Required for FF

  link.click()
}


export function downloadEntityBio (data, name) {
  let rows = data.map(d => {
    let crimes = d.delitos.join(' - ')

    return [d.expediente, d.anio_comienzo, d.juez.nombre, d.fiscal.nombre, d.relacion,
            crimes, d.estado, d.ultima_actualizacion]
  })

  let header = ['expediente', 'anio_comienzo', 'juez', 'fiscal', 'relacion',
                'delitos', 'estado', 'ultima_actualizacion']

  let csvName = `${name.toLowerCase()} bio.csv`

  generateCSV(csvName, header, rows)
}


export function downloadEntityCases (data, name) {
  let rows = data.map(d => {
    let crimes = d.delitos.join(' - ')

    let denu = d.involucrados.filter(d => d.relacion === 'denunciante')
      .map(d => d.nombre)
      .join(' - ')

    let quere = d.involucrados.filter(d => d.relacion === 'querellante')
      .map(d => d.nombre)
      .join(' - ')

    let invest = d.involucrados.filter(d => d.relacion === 'investigado')
      .map(d => d.nombre)
      .join(' - ')

    return [d.anio_comienzo, d.expediente, d.juez.nombre, d.fiscal.nombre, crimes,
      d.relacion, denu, quere, invest, d.estado, d.ultima_actualizacion]
  })

  let header = ['anio_comienzo', 'expediente', 'juez', 'fiscal', 'delitos',
    'relacion', 'denunciantes', 'querellantes', 'investigado', 'estado', 'ultima_actualizacion']

  let csvName = `${name.toLowerCase()} causas.csv`

  generateCSV(csvName, header, rows)
}


export function downloadCasesResolution (data, name) {
  let rows = data.map(d => {
    let date = d.fecha_resolucion.getDate() + '/' + d.fecha_resolucion.getMonth()
       + '/' + d.fecha_resolucion.getFullYear()

    return [date, d.camara, d.sala, `"${d.resuelve_texto.replace('"', "'")}"`, d.pdf_link]
  })

  let header = ['fecha_resolucion', 'camara', 'sala', 'resuelve_texto', 'pdf_link']

  let csvName = `${name.toLowerCase()} resoluciones.csv`

  generateCSV(csvName, header, rows)
}


export function downloadCasesInvolved (data, name) {
  let rows = data.map(d => {
    return [d.nombre, d.relacion]
  })

  let header = ['nombre', 'relacion']

  let csvName = `${name.toLowerCase()} relaciones.csv`

  generateCSV(csvName, header, rows)
}


export function downloadStats (data, name) {
  let rows = data.map(d => [d.name, d.value])

  let header = ['nombre', 'valor']
  let csvName = `estadisticas ${name}.csv`

  generateCSV(csvName, header, rows)
}


export function downloadStatsOral (data, name) {
  let rows = data.map(d => [d.name, d.juicio_oral, d.total])

  let header = ['nombre_juez', 'juicios_oral', 'juicio_total']
  let csvName = `estadisticas ${name}.csv`

  generateCSV(csvName, header, rows)
}


export function downloadStatsOld (data, name) {
  let rows = data.map(d => [new Date().getFullYear() - d.anio_comienzo, d.expediente, `"${d.caratula}"`])

  let header = ['anios_abierto', 'expediente', 'caratula']
  let csvName = `estadisticas ${name}.csv`

  generateCSV(csvName, header, rows)
}

export function downloadGraph (data, name) {
  let rows = data.map(d => {
    return [d.source.id, d.target.id, d.tipo, d.source.tipo, d.source.subtipo,
            d.source.metricas.degree, d.target.tipo, d.target.subtipo, d.target.metricas.degree]
  })

  let header = ['source', 'target', 'relacion', 'source_tipo', 'source_subtipo',
    'source_degree', 'target_tipo', 'target_subtipo', 'target_degree']

  let csvName = `${name.toLowerCase()} conecciones.csv`

  generateCSV(csvName, header, rows)
}
