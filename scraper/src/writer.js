import fs from 'fs'

const clear_line = (line) =>
  line
    .map((val) => {
      try {
        return val.replace(/"/g, ' ').replace(/\n/g, ' ')
      } catch (error) {
        return val
      }
    })
    .join('","')

const streams = {}
const outputDir = 'data'
const keys = [
  'causas',
  'delitos',
  'radicacioon_del_expediente',
  'resoluciones',
  'implicados',
]

if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir)
}

keys.forEach((key) => {
  streams[key] = fs.createWriteStream(`${outputDir}/${key}.csv`, { flags: 'a' })
})

const write = (entry) => {
  const lines = {}
  entry.causas = [
    {
      estado: entry.estado,
      ultima_actualizacion: entry.ultima_actualizacion,
      caratula: entry.caratula,
      terminado: entry.terminado,
    },
  ]

  keys.forEach((key) => {
    if (key in entry) {
      lines[key] = entry[key].map((e) => ({
        expediente: entry.expediente,
        ...e,
      }))
    }
  })

  Object.keys(lines).forEach((key) => {
    lines[key].forEach((line) => {
      if (fs.readFileSync(`${outputDir}/${key}.csv`).length === 0) {
        const header = clear_line(Object.keys(line))
        streams[key].write(`"${header}"\n`)
      }

      line = clear_line(Object.values(line))
      streams[key].write(`"${line}"\n`)
    })
  })
}

export default write
