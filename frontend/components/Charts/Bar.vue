<template>
  <svg :id="id"></svg>
</template>

<script>
import * as d3 from 'd3'
import { wrapText } from '@/assets/utils'

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
    maxVal: {
      type: Number,
      default: -1
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
      .attr('fill', 'steelblue')

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
      // Sort the data
      let data = this.data.slice()
      data.sort((a, b) => a.value - b.value)

      let maxVal
      if (this.maxVal !== -1) {
        maxVal = this.maxVal
      } else {
        maxVal = d3.max(data, d => d.value)
      }

      let x = d3.scaleLinear()
        .domain([0, maxVal])
        .rangeRound([this.margin.left, this.width - this.margin.right])

      let y = d3.scaleBand()
        .domain(data.map(d => d.name))
        .rangeRound([this.height - this.margin.bottom, this.margin.top])
        .padding(0.1)

      // Bars
      let bar = this.svg.select('.bars')
        .selectAll('rect')
        .data(data)

      bar.enter()
        .append('rect')
        .merge(bar)
        .attr('x', x(0))
        .attr('y', d => y(d.name))
        .attr('width', d => x(d.value) -x(0))
        .attr('height', y.bandwidth())

      bar.exit().remove()

      // Text on the end of each bar
      let text = this.svg.select('.labels')
        .selectAll('text')
        .data(data)

      text.enter()
        .append('text')
        .merge(text)
        .attr("x", d => x(d.value) - 30)
        .attr("y", d => y(d.name) + y.bandwidth() / 2)
        .attr("dy", "0.35em")
        .text(d => d.value )

      text.exit().remove()

      // Update the axis
      this.svg.selectAll('.axis')
        .selectAll('.tick')
        .remove()

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

      // Remove domain and lines on axis
      // this.svg.select('.axis-y')
      //   .select('.domain')
      //   .remove()
      // this.svg.selectAll('.axis')
      //   .selectAll('line')
      //   .remove()
    }
  }
}
</script>
