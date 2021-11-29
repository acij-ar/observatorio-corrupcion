<template>
  <svg :id="id"></svg>
</template>

<script>
import * as d3 from 'd3'

export default {
  data () {
    return {
      svg: null,
      svgSize: { width: 0, height: 0 },
      margin: { top: 40, right: 40, bottom: 40, left: 40 }
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
    }
  },
  watch: {
    data: function () {
      this.draw()
    }
  },
  mounted () {
    // SVG size
    let divW = document.getElementsByClassName('container')[0].clientWidth
    this.svgSize = {
      width: divW - this.margin.left,
      height: divW
    }

    /**
    this.svgSize = {
      width: divW - this.margin.left - this.margin.right,
      height: divW * 5 - this.margin.top - this.margin.bottom
    }*/

    // Set SVG
    this.svg = d3.select(`#${this.id}`)
      .attr('width', this.svgSize.width + this.margin.left + this.margin.right)
      .attr('height', this.svgSize.height + this.margin.top + this.margin.bottom)

    this.draw()
  },
  methods: {
    draw: function () {
      let format = d3.format(',d')

      let pack = data => d3.pack()
        .size([this.svgSize.width - 170, this.svgSize.height - 150])
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
        .selectAll('tspan')
        .attr('font-family', 'MontserratRegular')        
        .data(d => `Cantidad: ${d.value}`)
        .enter().append('tspan')
          .attr('x', (d, i, nodes) => `${i - nodes.length / 2}em`)
          .attr('y', d => 0)
          .text(d => d);

      leaf.append('title')
        .text(d => d.data.name.concat([`\nCantidad: ${d.value}`]))
    }
  }
}
</script>
