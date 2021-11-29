<template>
  <div>
    <p>
      Causas de corrupcion, cerradas o abiertas, que involucran a {{ this.name }}
      segun su año de comienzo. Los colores de los círculos indican el tipo de
      relacion que tiene con cada causa y los colores de fondo corresponden al
      período presidencial en el que se inició.
      Posando el mouse sobre cada círculo podes ver más información de la causa correspondiente.
    </p>

    <svg id="casesEvolution"></svg>
  </div>
</template>

<script>
import * as d3 from 'd3'

export default{
  name: 'CasesEvolution',
  data () {
    return {
      // SVG
      svg: null,
      g: null,
      svgSize: {width: 0, height: 0},
      margin: {top: 30, right: 160, bottom: 30, left: 60}
    }
  },
  props: {
    cases: {
      type: Array,
      required: true
    },
    name: {
      type: String,
      required: true
    }
  },
  watch: {
    cases: function () {
      this.draw()
    }
  },
  mounted () {
    // Create the base svg elements
    // SVG size
    let divW = document.getElementsByClassName('columns')[0].clientWidth
    this.svgSize = {
      width: divW - this.margin.left - this.margin.right,
      height: (divW / 3) - this.margin.top - this.margin.bottom
    }

    // Set SVG
    this.svg = d3.select('#casesEvolution')
      .attr('width', this.svgSize.width + this.margin.left + this.margin.right)
      .attr('height', this.svgSize.height + this.margin.top + this.margin.bottom)

    this.g = this.svg.append('g')
      .attr('transform', `translate(${this.margin.left}, ${this.margin.top})`)

    // Append x-axis
    this.g.append('g')
      .attr('class', 'axis axis-x')
      .attr('transform', `translate(0, ${this.svgSize.height})`)

    // Append y-axis
    this.g.append('g')
      .attr('class', 'axis axis-y')
      .append('text')
      .attr('fill', '#000')
      .attr('transform', 'rotate(-90)')
      .attr('y', 0)
      .attr('dy', '-2.5em')
      .attr('text-anchor', 'end')
      .text('Cantidad de Causas')

    // Append base elements
    this.g.append('g')
      .attr('class', 'bars')

    this.g.append('g')
      .attr('class', 'bars-head')

    this.g.append('g')
      .attr('class', 'bars-text')

    this.g.append('g')
      .attr('class', 'dots')

    // Append legend
    this.svg.append('g')
      .attr('class', 'labels')
      .attr('transform', 'translate(200, 0)')
      .append('rect')

    this.draw()
  },
  methods: {
    draw: function () {
      let {data, colors} = this.parseData()

      let yMax = d3.max(data, d => d.value ) + 1
      let xMax = d3.max(data, d => d.anio_comienzo)
      let xMin = d3.min(data, d => d.anio_comienzo) - 1

      let dataBarPresidents = [
        { start: 1995, end: 1999, color: '#a1b5ff', color2: 'blue', president: 'PJ', textColor: 'white'},
        { start: 1999, end: 2001, color: '#ccebc5', color2: 'green', president: 'Alianza', textColor: 'white'},
        { start: 2001, end: 2003, color: '#a1b5ff', color2: 'blue', president: 'PJ', textColor: 'white'},
        { start: 2003, end: 2007, color: '#b8b8ff', color2: 'blue', president: 'FPV', textColor: 'white' },
        { start: 2007, end: 2011, color: '#b8b8ff', color2: 'blue', president: 'FPV', textColor: 'white'  },
        { start: 2011, end: 2015, color: '#b8b8ff', color2: 'blue', president: 'FPV', textColor: 'white'  },
        { start: 2015, end: 2019, color: '#ffffb0', color2: 'yellow', president: 'Cambiemos', textColor: 'black'  },
        { start: 2019, end: 2023, color: '#b8b8ff', color2: 'blue', president: 'Todos', textColor: 'white'  }
      ]

      let indexS = dataBarPresidents.findIndex(d => (d.start <= xMin) && (xMin <= d.end))
      let indexE = dataBarPresidents.findIndex(d => (d.start <= xMax) && (xMax <= d.end))
      dataBarPresidents = dataBarPresidents.slice(indexS, indexE + 1)

      // X lim
      let xStart = dataBarPresidents[0].start
      let xEnd = dataBarPresidents[dataBarPresidents.length - 1].end

      //
      let x = d3.scaleLinear()
        .range([0, this.svgSize.width])
        .domain([xStart, xEnd])

      let y = d3.scaleLinear()
        .range([this.svgSize.height, 0])
        .domain([0.5, yMax])

      let format = d3.format('d')

      // Bar head
      let barHead = this.g.select('.bars-head')
        .selectAll('.bar')
        .data(dataBarPresidents)

      barHead.enter()
        .append('rect')
        .attr('class', 'bar')
        .merge(barHead)
        .attr('x', d => x(d.start))
        .attr('y', d => -this.margin.top)
        .attr('width', d => x(d.start + 4) - x(d.start))
        .attr('height', d => this.margin.top)
        .style('fill', d => d.color2)

      barHead.exit()
        .remove()

      // Bar head text
      let barText = this.g.select('.bars-text')
        .selectAll('text')
        .data(dataBarPresidents)

      barText.enter()
        .append('text')
        .merge(barText)
        .attr('x', d => x(d.start + (d.end - d.start) / 2))
        .attr('y', d => -this.margin.top / 2)
        .attr('dy', '0.35em')
        .attr('text-anchor', 'middle')
        .style('fill', d => d.textColor)
        .text(d => d.president)

      barText.exit()
        .remove()

      // Bar for president periode
      let bar = this.g.select('.bars')
        .selectAll('.bar')
        .data(dataBarPresidents)

      // Enter + update
      bar.enter()
        .append('rect')
        .attr('class', 'bar')
        .merge(bar)
        .attr('x', d => x(d.start))
        .attr('y', d => y(yMax))
        .attr('width', d => x(d.start + 4) - x(d.start))
        .attr('height', d => this.svgSize.height - y(yMax))
        .style('fill', d => d.color)

      bar.exit()
        .remove()

      // Append circles
      let dots = this.g.select('.dots')
        .selectAll('.dot')
        .data(data)

      dots.enter()
        .append('circle')
        .attr('class', 'dot')
        .merge(dots)
        .attr('r', 8)
        .attr('cx', d => x(d.anio_comienzo))
        .attr('cy', d => y(d.value))
        .attr('stroke', 'black')
        .attr('stroke-width', 2)
        .attr('fill', d => colors[d.relacion])
        .on('mouseover', d => this.mouseover(d))
        .on('mouseout', d => this.mouseout(d))

      dots.exit()
        .remove()

      // Update x-axis
      this.g.select('.axis-x')
        .call(d3.axisBottom(x).tickFormat(format))

      // Update y-yxis
      this.g.select('.axis-y')
        .call(d3.axisLeft(y).tickFormat(value => {
          return Math.floor(value) == value ? value : ''
        }))

      // Remove domain on axis
      d3.selectAll('.axis').select('.domain').remove()
      d3.selectAll('.axis').select('g').remove()
      d3.selectAll('.axis').selectAll('line').remove()


      // Remove old labels
      this.svg.select('.labels')
        .selectAll('.legend')
        .remove()

      this.svg.select('.labels')
        .select('rect')
        .attr('x', 0)
        .attr('y', 0)
        .attr('width', 0)
        .attr('height', 0)

      // Update the legend
      let legend = this.svg.select('.labels')
        .selectAll('.legend')
        .data(Object.keys(colors))
        .enter().append('g')
        .attr('class', 'legend')
        .attr('transform', (d, i) => `translate(0, ${10 + i * 20})`)

      legend.append('circle')
        .attr('r', 8)
        .attr('cx', this.svgSize.width)
        .attr('cy', 10)
        .style('fill', d => colors[d])

      legend.append('text')
        .attr('x', this.svgSize.width - 20)
        .attr('y', 9)
        .attr('dy', '.35em')
        .style('text-anchor', 'end')
        .text(d => d)

      // Legend background rect
      let bbox
      this.svg.select('.labels')
        .each(function(d) { bbox = [this.getBBox()] })
        .data(bbox)
        .select('rect')
        .attr('x', d => d.x - 9)
        .attr('y', d => 2)
        .attr('width', d => d.width + 20)
        .attr('height', d => d.height + 20)
    },
    mouseover: function (d) {
      /*
        On mouse over highlight the rect and shoe the tooltip
      */
      // Update the tooltip position and value
      d3.select('#tooltip')
        .style('left', (d3.event.pageX - 125) + 'px')
        .style('top', (d3.event.pageY + 20) + 'px')
        .select('#value')
        .html(() => {
          return `<strong>Caratula:</strong> ${d.nombre}<br /><strong>Estado:</strong> ${d.estado}<br />
          <strong>Juez:</strong> ${d.juez.nombre}<br /><strong>Fiscal:</strong> ${d.fiscal.nombre}`
        })

      // Show the tooltip
      d3.select('#tooltip').classed('hidden', false)
    },
    mouseout: function (d) {
      /*
        On mouse out, remove the highlight
      */
      d3.select('#tooltip').classed('hidden', true)
    },
    parseData: function () {
      // Prepareted the data
      let data = this.cases.slice()
      data = data.map(d => {
        d.relacion = d.relacion.replace(/denunciado|imputado|procesado|denunciado/, 'investigado/a')
        return d
      })

      // data.forEach(d => { d.anio_comienzo = parseInt(d.anio_comienzo) })

      // Sort the data by multiple fields. Ty to
      // https://bytemaster.io/javascript-object-multi-property-sort
      let sortBy = [{
        prop:'anio_comienzo',
        direction: 1
      },{
        prop:'relacion',
        direction: 1
      }]

      data.sort((a,b) => {
        let i = 0
        let result = 0
        while(i < sortBy.length && result === 0) {
          result = sortBy[i].direction * (a[sortBy[i].prop].toString() < b[sortBy[i].prop].toString() ? -1
            : a[sortBy[i].prop].toString() > b[sortBy[i].prop].toString() ? 1
              : 0)
          i++;
        }
        return result
      })

      // Calculo las causas por anio
      var years = new Set()
      data.forEach(cases => {
        years.add(cases.anio_comienzo)
      })

      years.forEach(year => {
        let byYear = data.filter(cases => { return cases.anio_comienzo === year })
        byYear.forEach((cases, index) => {
          cases.value = index + 1
        })
      })

      let colors = {
        'juez': '#377eb8',
        'fiscal': '#ffff33',
        'denunciante': '#e41a1c',
        'querellante': '#4daf4a',
        'sobreseido': '#984ea3',
        'investigado/a': '#ff7f00'
      }

      // Filtro las labels que aparecen
      let relations = new Set()
      this.cases.forEach(d => relations.add(d.relacion))

      colors = Object.keys(colors)
        .filter(key => relations.has(key))
        .reduce((obj, key) => {
          obj[key] = colors[key]
          return obj
        }, {})

      return { data, colors }
    }
  }
}
</script>

<style scoped>
p {
  padding-bottom: 30px;
}
</style>
