<template>
  <svg :id="id" />
</template>

<script>
import * as d3 from 'd3'

export default {
  data () {
    return {
      svg: null,
      // g: null,
      svgSize: { width: 0, height: 0 },
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
      default: 800,
    },
    height: {
      type: Number,
      default: 800,
    },
  },
  watch: {
    data: function () {
      this.draw()
    }
  },
  mounted () {
    this.svg = d3.select(`#${this.id}`)
      .attr("width", this.width)
      .attr("height", this.height)
      .attr("viewBox", [0, 0, this.width, this.height])
      .attr("style", "max-width: 100%; height: auto; height: intrinsic;")

    this.svg.append('g')
      .attr('class', 'arcs')
      .attr('transform', `translate(${this.width / 2}, ${this.height / 2})`)

    this.draw()
  },
  methods: {
    draw: function () {
      const radius = Math.min(this.width, this.height) / 2

      const pie = d3.pie()
        .sort(null)
        .value(d => d.value)

      const path = d3.arc()
        .outerRadius(40*radius/100)
        .innerRadius(radius)

      const arc = this.svg.select('.arcs')
        .selectAll(".arc")
        .data(pie(this.data))

      arc.enter()
        .append("path")
        .merge(arc)
        .attr("d", path)
        .attr('fill', d => d3.schemeCategory10[d.index])

      arc.exit().remove()
    }
  }
}
</script>

<style scoped>
svg {
  max-height: 350px;
}
</style>
