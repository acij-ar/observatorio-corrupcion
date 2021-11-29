/*
  Commons functions, values
*/
import * as d3 from 'd3'
import axios from 'axios'

// baseUrl and apiUrl depending if production or not
export const apiUrl = process.env.NODE_ENV === 'production'
  ? 'http://api.causasdecorrupcion.org/v1/'
  : 'http://0.0.0.0:5000/v1/'

export const baseUrl = process.env.NODE_ENV === 'production'
  ? '/'
  : '/'

export const HTTP = axios.create({
  baseURL: apiUrl
})

export function getEntity () {
  HTTP.get(`nodo/nodos_entidades/${this.$route.query.nombre}`)
    .then(response => {
      let entity = response.data.entidad

      // Short name
      entity.causas = entity.causas.map(d => {
        d.juez = Object.keys(renameJudges).includes(d.juez) ? renameJudges[d.juez]
          : d.juez

        d.fiscal = Object.keys(renameFiscal).includes(d.fiscal) ? renameFiscal[d.fiscal]
          : d.fiscal
        return d
      })

      this.entity = entity

      // Page state
      this.isError = false
      this.isLoading = false
    })
    .catch(error => {
      // Page state
      this.isError = true
      this.isLoading = false
      this.errors.push(error)
    })
}

export function getCases () {
  HTTP.get('nodo/nodos_causas/' + this.$route.query.nombre)
    .then(response => {
      this.cases = response.data.causa

      this.cases.link = this.cases.expediente.replace('/', '-')
      this.cases.foto = this.cases.nombre_causa != '' ? this.cases.link + '.jpg' : 'nn.png'

      this.cases.resoluciones = this.cases.resoluciones.map(d => {
        let f = d.fecha.split('/')
        d.fecha_resolucion = new Date(f[2], f[1], f[0])

        return d
      })

      // Page state
      this.isReady = true
      this.isLoading = false
    })
    .catch(error => {
      // Page state
      this.isError = true
      this.isLoading = false
      this.errors.push(error)
    })
}

export function getMagistrate () {
  HTTP.get(`nodo/nodos_magistrados/${this.$route.query.nombre}`)
    .then(response => {
      this.magistrate = response.data.magistrado

      if (this.magistrate.foto === '') {
        this.magistrate.foto = 'nn.png'
      }

      // Page state
      this.isError = false
      this.isLoading = false
    })
    .catch(error => {
      // Page state
      this.isError = true
      this.isLoading = false
      this.errors.push(error)
    })
}

export function wrapText (text, width, lineHeight=1.1, dy=1) {
  /*
  Break long label in multiple lines.
  This code was take from https://bl.ocks.org/mbostock/7555321
  Thanks to Mike Bostock!
  */
  text.each(function () {
    let text = d3.select(this)
    let words = text.text().split(/\s+/).reverse()
    let word
    let line = []
    let lineNumber = 0
    // let lineHeight = 1.1
    let y = text.attr('y')
    let x = text.attr('x') || 0
    // let dy = 1

    let tspan = text.text(null)
      .append('tspan')
      .attr('x', x)
      .attr('y', y)
      // .attr('dy', dy + 'em')
      .attr('dy', '0em')

    // eslint-disable-next-line
    while (word = words.pop()) {
      line.push(word)
      tspan.text(line.join(' '))
      if (tspan.node().getComputedTextLength() - x > width) {
        line.pop()
        tspan.text(line.join(' '))
        line = [word]
        tspan = text.append('tspan')
          .attr('x', x)
          .attr('y', y)
          // .attr('dy', ++lineNumber * lineHeight + dy + 'em')
          .attr('dy', dy + 'em')
          .text(word)
      }
    }
  })
}

export const renameJudges = {
  'SERVINI DE CUBRÍA MARÍA R': 'MARIA SERVINI DE CUBRÍA',
  'RAFECAS DANIEL EDUARDO': 'DANIEL E. RAFECAS',
  'TORRES SERGIO G': 'SERGIO G. TORRES',
  'RODRIGUEZ LUIS OSVALDO': 'LUIS O. RODRIGUEZ',
  'CANICOBA CORRAL RODOLFO A': 'CORRAL R. CANICOBA',
  'MARTINEZ DE GIORGI MARCELO PEDRO HERNÁN': 'MARCELO M. DE GIORGI',
  'ERCOLINI JULIÁN DANIEL': 'JULIÁN D. ERCOLINI',
  'RAMOS SEBASTIÁN ROBERTO': 'SEBASTIÁN R. RAMOS',
  'CASANELLO SEBASTIÁN NORBERTO': 'SEBASTIÁN CASANELLO',
  'LIJO ARIEL OSCAR': 'ARIEL O. LIJO',
  'BONADÍO CLAUDIO': 'CLAUDIO BONADÍO'
}

const renameFiscal = {
  "STORNELLI CARLOS ERNESTO": "CARLOS E. STORNELLI",
  "DELGADO FEDERICO JOSÉ": "FEDERICO J. DELGADO",
  "RIVOLO CARLOS ALBERTO": "CARLOS A. RIVOLO",
  "OCHOA MARÍA PALOMA": "MARÍA P. OCHOA",
  "PICARDI FRANCO EDUARDO": "FRANCO E. PICARDI",
  "POLLICITA GERARDO DAVID": "GERARDO POLLICITA",
  "MANGANO MARÍA ALEJANDRA": "MARÍA MANGANO",
  "TAIANO EDUARDO RAÚL": "EDUARDO R. TAIANO",
  "MARIJUAN GUILLERMO FERNANDO": "GUILLERMO MARIJUAN",
  "DI LELLO JORGE FELIPE": "JORGE F. DI LELLO",
  "RECCHINI PABLO GABRIEL": "PABLO G. RECCHINI",
  "MARIA JOSEFINA MINATTA": "JOSEFINA M. MARIA",
  "ALDO GUSTAVO DE LA FUENTE": "GUSTAVO FUENTE ALDO",
  "MARIA MARTA SCHIANNI": "MARIA M. SCHIANNI",
  "ANDRADES ESTELA GLORIA": "ESTELA G. ANDRADES",
  "JORGE DAHL ROCHA": "JORGE ROCHA",
  "EDUARDO JOSE VILLALBA": "EDUARDO J. VILLALBA.",
  "LÓPEZ PERRANDO MARTÍN": "PERRANDO M. LÓPEZ",
  "RUILÓPEZ MARCELO ALBERTO": "MARCELO RUILÓPEZ",
  "ZONI JUAN PEDRO": "JUAN P. ZONI",
  "ROSENDE EDUARDO ENRIQUE": "EDUARDO E. ROSENDE"
}
