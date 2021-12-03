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
      .attr('width', this.svgSize.width)
      .attr('height', this.svgSize.height)
  },
  methods: {
    draw: function () {
      let series = d3.stack().keys(this.data.columns.slice(1))(this.data)

      let yAxis = g => g
        .attr("transform", `translate(${this.margin.left},0)`)
        .call(d3.axisLeft(y).ticks(null, "s"))
        .call(g => g.selectAll(".domain").remove())

      let xAxis = g => g
        .attr("transform", `translate(0,${this.svgSize.height - this.margin.bottom})`)
        .call(d3.axisBottom(x).tickSizeOuter(0))
        // .call(wrapText, x.bandwidth())
        .call(g => g.selectAll(".domain").remove())

      let x = d3.scaleBand()
        .domain(this.data.map(d => d.name))
        .range([this.margin.left, this.svgSize.width - this.margin.right])
        .padding(0.1)

      let y = d3.scaleLinear()
        .domain([0, d3.max(series, d => d3.max(d, d => d[1]))])
        .rangeRound([this.svgSize.height - this.margin.bottom, this.margin.top])

      let color = d3.scaleOrdinal()
        .domain(series.map(d => d.key))
        .range(d3.quantize(t => d3.interpolateSpectral(t * 0.8 + 0.1), series.length).reverse())
        .unknown("#ccc")

      this.svg.append('g')
        .selectAll("g")
        .data(series)
        .enter().append('g')
        .attr("fill", d => color(d.key))
        .selectAll("rect")
        .data(d => d)
        .enter().append('rect')
      .attr("x", (d, i) => x(d.data.name))
      .attr("y", d => y(d[1]))
      .attr("height", d => y(d[0]) - y(d[1]))
      .attr("width", x.bandwidth())

      this.svg.append("g")
        .call(xAxis)

      this.svg.append("g")
         .call(yAxis)
    }
  }
}
</script>
