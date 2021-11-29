<template>
  <svg :id="id"></svg>
</template>

<script>
import * as d3 from 'd3'

export default {
  data () {
    return {
      svg: null,
      g: null,
      svgSize: { width: 0, height: 0 },
      margin: { top: 20, right: 20, bottom: 20, left: 20 }
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
    const width = 400
    const height = 400
    this.svgSize = { width: width, height: height }

    this.svg = d3.select(`#${this.id}`)
      .attr('width', width)
      .attr('height', height)

    this.g = this.svg.append('g')
      .attr('transform', `translate(${width/2}, ${height/2})`)
  },
  methods: {
    draw: function () {
      const radius = Math.min(this.svgSize.width, this.svgSize.height) / 2

      var pie = d3.pie()
        .sort(null)
        .value(d => d.value)

      var path = d3.arc()
        .outerRadius(40*radius/100)
        .innerRadius(radius)

      var arc = this.g.selectAll(".arc")
        .data(pie(this.data))
        .enter()
          .append("g")
          .attr("class", "arc")

      arc.append("path")
        .attr("d", path)
        .attr('fill', d => d3.schemeCategory10[d.index])
    }
  }
}
</script>
