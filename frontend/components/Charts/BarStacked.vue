<template>
  <svg :id="id"></svg>
</template>

<script>
import * as d3 from 'd3'
import { wrapText } from '~/assets/utils'

export default {
  data () {
    return {
      svg: null,
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
    width: {
      type: Number,
      default: 1200,
    },
    height: {
      type: Number,
      default: 450,
    },
    margin: {
      type: Object,
      default: () => ({ top: 20, right: 40, bottom: 40, left: 250 })
    },
    xLabel: {
      type: String,
      default: 'Cantidad de causas'
    },
    mouseover: {
      type: Function,
      default: () => {}
    },
    mouseout: {
      type: Function,
      default: () => d3.select('#tooltip').classed('hidden', true)
    }
  },
  watch: {
    data: function () {
      this.draw()
    }
  },
  mounted () {
    // Set SVG
    this.svg = d3.select(`#${this.id}`)
      .attr("width", this.width)
      .attr("height", this.height)
      .attr("viewBox", [0, 0, this.width, this.height])
      .attr("style", "max-width: 100%; height: auto; height: intrinsic;")

    // For bars
    this.svg
      .append('g')
      .attr('class', 'bars')

    this.svg
      .append('g')
      .attr('class', 'labels')
      .attr('fill', 'white')

    // For axis
    this.svg
      .append('g')
      .attr('class', 'axis axis-x')
      .attr('transform', `translate(0, ${this.height - this.margin.bottom})`)

    this.svg
      .append('g')
      .attr('class', 'axis axis-y')
      .attr('transform', `translate(${this.margin.left}, 0)`)

    this.draw()
  },
  methods: {
    draw: function () {
      let data = this.data.slice()
      data.columns = this.data.columns
      data.sort((a, b) => a.total - b.total)

      let series = d3.stack()
        .keys(data.columns.slice(1))(data)

      let x = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.total)])
        .rangeRound([this.margin.left, this.width - this.margin.right])

      let y = d3.scaleBand()
        .domain(data.map(d => d.name))
        .rangeRound([this.height - this.margin.bottom, this.margin.top])
        .padding(0.1)

      let color = d3.scaleOrdinal()
        .domain(series.map(d => d.key))
        .range(d3.quantize(t => d3.interpolateSpectral(t * 0.8 + 0.1), series.length).reverse())
        .unknown("#ccc")

      // Bars
      let bar = this.svg.select('.bars')
        .selectAll('g')
        .data(series)
        .enter()
          .append("g")
          .attr("fill", d =>  color(d.key))
        .selectAll('rect')
        .data(d => d)

      bar.enter()
        .append('rect')
        .merge(bar)
        .attr('x', d => x(d[0]))
        .attr('y', d => y(d.data.name))
        .attr('width', d => x(d[1]) - x(d[0]))
        .attr('height', y.bandwidth())
        .on('mouseover', d => this.mouseover(d))
        .on('mouseout', d => this.mouseout(d))

      bar.exit().remove()

      // Text on the end of each bar
      let text = this.svg.select('.labels')
        .selectAll('text')
        .data(series.flat())

      text.enter()
        .append('text')
        .merge(text)
        .attr("x", d => x(d[1]) - x(d[1])*0.04)
        .attr("y", d => y(d.data.name) + y.bandwidth() / 2)
        .attr("dy", "0.35em")
        .text(d => d[1] - d[0] )

      text.exit().remove()

      // Update the axis
      this.svg.select('.axis-x')
      .call(d3.axisBottom(x))
      .call(g => g.select(".domain").remove())
      .call(g => g.selectAll(".tick line").clone()
          .attr("y1", -(this.height - this.margin.bottom - this.margin.top))
          .attr("y2", 0)
          .attr("stroke-opacity", 0.1))
      .call(g => g.append("text")
          .attr("x", this.width - this.margin.right)
          .attr("y", -22)
          .attr("fill", "currentColor")
          .attr("text-anchor", "end")
          .text(this.xLabel))

      this.svg.select('.axis-y')
        .call(d3.axisLeft(y))
        .selectAll('text')
        .text(d => d.toUpperCase())
        .call(wrapText, this.margin.left, 1.2)
    },
  }
}
</script>
