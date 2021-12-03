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
      // g: null,
      // svgSize: {width: null, height: null},
      // margin: {top: 20, right: 20, bottom: 100, left: 50}
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
      default: 600,
    },
    margin: {
      type: Object,
      default: () => ({ top: 20, right: 20, bottom: 100, left: 50 })
    },
    yLabel: {
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
      // Create the axis
      let x = d3.scaleBand()
        .domain(this.data.map(d => d.name))
        .rangeRound([this.margin.left, this.width - this.margin.right])
        .padding(0.1)

      let y = d3.scaleLinear()
        .domain([0, d3.max(this.data, d => d.value)])
        .rangeRound([this.height - this.margin.bottom, this.margin.top])

      // Bars
      let bar = this.svg.selectAll('.bars')
        .selectAll('rect')
        .data(this.data)

      bar.enter()
        .append('rect')
        .merge(bar)
        .attr('x', d => x(d.name))
        .attr('y', d => y(d.value))
        .attr('width', x.bandwidth())
        .attr('height', d => y(0) - y(d.value))

      bar.exit().remove()

      // Text on the end of each bar
      let text = this.svg.select('.labels')
        .selectAll('text')
        .data(this.data)

      text.enter()
        .append('text')
        .merge(text)
        .text(d => d.value )
        .attr("x", function(d) {
          return x(d.name) + (x.bandwidth() / 2) - (this.getComputedTextLength() / 2)
        })
        .attr("y", d => y(d.value) + 30)

      text.exit().remove()

      // Update the axis
      this.svg.select('.axis-x')
        .call(d3.axisBottom(x))
        .selectAll('.tick text')
        .call(wrapText, x.bandwidth())

      this.svg.select('.axis-x')
        .selectAll('.tick tspan')
        .attr('dy', '1em')

      this.svg.select('.axis-y')
        .call(d3.axisLeft(y))
        .call(g => g.select(".domain").remove())
        .call(g => g.selectAll(".tick line").clone()
            .attr("x2", this.width - this.margin.left - this.margin.right)
            .attr("stroke-opacity", 0.1))
        .call(g => g.append("text")
            .attr("x", -this.margin.left)
            .attr("y", 10)
            .attr("fill", "currentColor")
            .attr("text-anchor", "start")
            .text(this.yLabel))
    }
  }
}
</script>
