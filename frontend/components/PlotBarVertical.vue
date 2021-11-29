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
      g: null,
      svgSize: {width: null, height: null},
      margin: {top: 20, right: 20, bottom: 100, left: 50}
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
    }
  },
  watch: {
    data: function () {
      this.draw()
    }
  },
  mounted () {
    // SVG size
    let divW = d3.select(`#${this.id}`).node().parentNode.clientWidth
    this.svgSize = {
      width: divW - this.margin.left - this.margin.right,
      height: (divW / 2) - this.margin.top - this.margin.bottom
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
  },
  methods: {
    draw: function () {
      // Create the axis
      let x = d3.scaleBand()
        .domain(this.data.map(d => d.name))
        .rangeRound([0, this.svgSize.width])
        .padding(0.1)

      let y = d3.scaleLinear()
        .domain([0, d3.max(this.data, d => d.value)])
        .rangeRound([this.svgSize.height, 0])

      // Create the bar
      let bar = this.g.selectAll('.bar')
        .data(this.data)

      bar.enter()
        .append('rect')
        .attr('class', 'bar')
        .attr('fill', 'steelblue')
        .merge(bar)
        .attr('x', d => x(d.name))
        .attr('y', d => y(d.value))
        .attr('width', x.bandwidth())
        .attr('height', d => { return this.svgSize.height - y(d.value) })

      // Text on the end of each bar
      let text = this.g.selectAll('text')
        .data(this.data)

      text.enter()
        .append('text')
        .merge(text)
        .attr("x", d => x(d.name) + x.bandwidth() / 3)
        .attr("y", d => y(d.value) + 30)
        .attr("dy", "0.35em")
        .attr('fill', 'white')
        .text(d => d.value )

      // Update the axis
      this.g.select('.x.axis')
        .call(d3.axisBottom(x))
        .selectAll('.tick text')
        .call(wrapText, x.bandwidth())

      this.g.select('.y.axis')
        .call(d3.axisLeft(y))
    }
  }
}
</script>
