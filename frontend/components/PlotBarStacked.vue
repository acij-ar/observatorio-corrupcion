<template>
  <svg :id="id"></svg>
</template>

<script>
import * as d3 from 'd3'
import { wrapText } from '~/assets/utils'

export default {
  data () {
    return {
      g: null,
      svg: null,
      svgSize: { width: 0, height: 0 },
      margin: { top: 20, right: 40, bottom: 40, left: 200 }
    }
  },
  props: {
    id: {
      type: String,
      required: true
    },
    data: {
      type: Array,
      required: true
    },
    barWidth: {
      type: Number,
      default: 60
    }
  },
  watch: {
    data: function () {
      this.resize()
      this.draw()
    }
  },
  mounted () {
    // SVG size
    let divW = d3.select(`#${this.id}`).node().parentNode.clientWidth
    if (divW === 0) {
      divW = document.getElementsByClassName('container')[0].clientWidth
    }

    this.svgSize = {
      width: divW - this.margin.left - this.margin.right,
      height: this.data.length * this.barWidth - this.margin.top - this.margin.bottom
    }

    // Set SVG
    this.svg = d3.select(`#${this.id}`)
      .attr('width', this.svgSize.width + this.margin.left + this.margin.right)
      .attr('height', this.svgSize.height + this.margin.top + this.margin.bottom)

    this.g = this.svg.append('g')
      .attr('transform', `translate(${this.margin.left}, ${this.margin.top})`)

    // Append g for the axis
    this.g.append('g')
      .attr('class', 'x axis')
      .attr('transform', `translate(0, ${this.svgSize.height})`)

    this.g.append('g')
      .attr('class', 'y axis')
      .attr('transform', 'translate(0, -10)')

    this.draw()
  },
  methods: {
    resize: function () {
      let divW = d3.select(`#${this.id}`).node().parentNode.clientWidth
      this.svgSize = {
        width: divW - this.margin.left - this.margin.right,
        height: this.data.length * this.barWidth - this.margin.top - this.margin.bottom
      }

      // SVG size
      this.svg.attr('width', this.svgSize.width + this.margin.left + this.margin.right)
        .attr('height', this.svgSize.height + this.margin.top + this.margin.bottom)

      // Append g for the axis
      this.g.select('.x.axis')
        .attr('transform', `translate(0, ${this.svgSize.height})`)
    },
    draw: function () {
      let series = d3.stack().keys(this.data.columns.slice(1))(this.data)

      let x = d3.scaleLinear()
        .domain([0, d3.max(this.data, d => d.total)])
        .rangeRound([0, this.svgSize.width])

      let y = d3.scaleBand()
        .domain(this.data.map(d => d.name))
        .rangeRound([0, this.svgSize.height])
        .padding(0.1)

      let color = d3.scaleOrdinal()
        .domain(series.map(d => d.key))
        .range(d3.quantize(t => d3.interpolateSpectral(t * 0.8 + 0.1), series.length).reverse())
        .unknown("#ccc")

      this.g.append("g")
        .selectAll("g")
        .data(series)
        .enter().append("g")
          .attr("fill", d =>  color(d.key))
        .selectAll("rect")
        .data(d => d)
        .enter().append("rect")
          .attr("x", d => x(d[0]))
          .attr("y", d => y(d.data.name))
          .attr("width", d => x(d[1]) - x(d[0]))
          .attr("height", y.bandwidth())
          .on('mouseover', (d, i) => this.mouseover(this.data[i]))
          .on('mouseout', d => this.mouseout(d))

      // Update the axis
      this.g.select('.x.axis')
        .call(d3.axisBottom(x))

      this.g.select('.y.axis')
        .call(d3.axisLeft(y))
        .selectAll('text')
        .text(d => d.toUpperCase())
        .call(wrapText, this.margin.left, 1.2)

      // remove domain and lines on y axis
      this.g.select('.y.axis')
        .select('.domain')
        .remove()

      this.g.select('.y.axis')
        .selectAll('line')
        .remove()

      this.g.select('.x.axis')
        .selectAll('line')
        .remove()
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
          return `Causas a <strong>Juicio oral:</strong> ${d.juicio_oral}<br />
          <strong>Causas totales:</strong> ${d.total}`
        })

      // Show the tooltip
      d3.select('#tooltip').classed('hidden', false)
    },
    mouseout: function (d) {
      /*
        On mouse out, remove the highlight
      */
      d3.select('#tooltip').classed('hidden', true)
    }
  }
}
</script>
