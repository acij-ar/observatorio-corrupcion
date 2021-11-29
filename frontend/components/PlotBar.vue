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
      margin: { top: 20, right: 40, bottom: 40, left: 350 }
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
      default: 40
    },
    maxVal: {
      type: Number,
      default: -1
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
      height: this.data.length * this.barWidth - this.margin.top - this.margin.bottom + 50
    }

    // Set SVG
    this.svg = d3.select(`#${this.id}`)      
      .attr('width', this.svgSize.width + this.margin.left + this.margin.right)
      .attr('height', this.svgSize.height + this.margin.top + this.margin.bottom)

    this.g = this.svg.append('g')      
      .attr('transform', `translate(${this.margin.left}, ${this.margin.top})`)

    // Append g for the axis
    this.g.append('g')      
      .attr('class', 'axis axis-x')
      .attr('transform', `translate(0, ${this.svgSize.height})`)

    this.g.append('g')            
      .attr('class', 'axis axis-y')      
      .attr('transform', 'translate(-5, 0)')

    this.svg.append('text')          
      .attr('class', 'notation')
      .attr('x', this.svgSize.width + 60)
      .attr('y', this.svgSize.height + 60)
      .text('Cantidad de causas')

    this.draw()
  },
  methods: {
    resize: function () {
      // SVG size
      let divW = d3.select(`#${this.id}`).node().parentNode.clientWidth
      if (divW === 0) {
        divW = document.getElementsByClassName('container')[0].clientWidth
      }

      this.svgSize = {
        width: divW - this.margin.left - this.margin.right,
        height: this.data.length * this.barWidth - this.margin.top - this.margin.bottom
      }

      // Update dimensions
      this.svg.attr('width', this.svgSize.width + this.margin.left + this.margin.right)
        .attr('height', this.svgSize.height + this.margin.top + this.margin.bottom)

      this.g.select('.axis.axis-x')
        .attr('transform', `translate(0, ${this.svgSize.height})`)

      this.svg.select('.notation')
        .attr('x', this.svgSize.width + 60)
        .attr('y', this.svgSize.height + 60)
        .text('Cantidad de causas')
    },
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
        .rangeRound([0, this.svgSize.width])
        .domain([0, maxVal])

      let y = d3.scaleBand()
        .rangeRound([this.svgSize.height, 0])        
        .padding(0.1)
        .domain(data.map(d => d.name))

      // Bars
      let bar = this.g.selectAll('.bar')
        .data(data)        

      bar.enter()
        .append('rect')
        .attr('class', 'bar')
        .attr('fill', 'steelblue')
        .merge(bar)
        .attr('x', 0)
        .attr('height', y.bandwidth())
        .attr('y', d => y(d.name))
        .attr('width', d => x(d.value))

      bar.exit().remove()

      // Text on the end of each bar
      let text = this.g.selectAll('text')
        .data(data)

      text.enter()
        .append('text')
        .merge(text)
        .attr("x", d => x(d.value) - 30)
        .attr("y", d => y(d.name) + y.bandwidth() / 2)
        .attr("dy", "0.35em")
        .attr('fill', 'white')
        .text(d => d.value )

      text.exit().remove()

      this.g.selectAll('.axis')
        .selectAll('.tick')
        .remove()

      // Update the axis
      this.g.select('.axis-x')
        .call(d3.axisBottom(x).ticks(maxVal).tickFormat(d3.format('d')))

      this.g.select('.axis-y')
        .call(d3.axisLeft(y))
        .selectAll('text')        
        .text(d => d.toUpperCase())
        .call(wrapText, this.margin.left, 1.2)

      // Remove domain and lines on axis
      this.g.select('.axis-y')
        .select('.domain')
        .remove()

      this.g.selectAll('.axis')
        .selectAll('line')
        .remove()
    }
  }
}
</script>
