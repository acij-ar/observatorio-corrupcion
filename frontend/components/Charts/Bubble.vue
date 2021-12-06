<template>
  <svg :id="id"></svg>
</template>

<script>
import * as d3 from 'd3'
import { wrapText2 } from '@/assets/utils'

export default {
  data () {
    return {
      svg: null,
    }
  },
  props: {
    data: {
      type: Array,
      required: true
    },
    id: {
      type: String,
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
    // Set SVG
    this.svg = d3.select(`#${this.id}`)
      .attr("width", this.width)
      .attr("height", this.height)
      .attr("viewBox", [0, 0, this.width, this.height])
      .attr("style", "max-width: 100%; height: auto; height: intrinsic;")

    this.draw()
  },
  methods: {
    draw: function () {
      let pack = data => d3.pack()
        .size([this.width, this.height])
        .padding(3)
        (d3.hierarchy({children: data})
          .sum(d => d.value))

      const root = pack(this.data)

      const leaf = this.svg.selectAll('g')
        .data(root.leaves())
        .enter()
        .append('g')
        .attr('transform', d => `translate(${d.x + 1},${d.y + 1})`)

      leaf.append('circle')
        .attr('id', d => d.data.name.replace(/ /g, '_'))
        .attr('r', d => d.r)
        .attr('fill-opacity', 0.7)
        .attr('fill', (d, i) => d3.schemeCategory10[i % 10])

      leaf.append('clipPath')
        .attr('id', d => 'clip-' + d.data.name.replace(/ /g, '_'))
        .append('use')
        .attr('xlink:href', d => '#' + d.data.name.replace(/ /g, '_'))

      leaf.append('text')
        .attr('clip-path', d => 'url(#clip-' + d.data.name.replace(/ /g, '_') + ')')
        // .attr('x', d => -(d.r / 2))
        // .attr('y', d => -(d.r / 2))
        .text(d => `${d.value}`)
        // .text(d => `${d.value} ${d.data.name}`)
        // .call(wrapText2)

      leaf.append('title')
        .text(d => d.data.name.concat([`\nCantidad: ${d.value}`]))
    }
  }
}
</script>

<style scoped>
svg {
  display: block;
  margin: auto;
}
</style>
