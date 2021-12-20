<template>
  <svg :id="id"></svg>
</template>

<script>
import * as d3 from 'd3'

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
      .attr("font-size", 10)
      .attr("font-family", "sans-serif")
      .attr("text-anchor", "middle")

    this.draw()
  },
  methods: {
    draw () {
        const data = JSON.parse(JSON.stringify(this.data))
        // Compute the values.
        const D = d3.map(data, d => d);
        const V = data.map(row => row.value);
        const G = data.map(row => row.name)
        const I = d3.range(V.length).filter(i => V[i] > 0);

        // Unique the groups.
        const groups = I.map(i => G[i]);

        // Compute labels and titles.
        const L = data.map(d => [...d.name.split(), d.value.toLocaleString("es")].join(" "))
        const T = data.map(d => `${d.name}\n${d.value.toLocaleString("es")}`)

        // Compute layout: create a 1-deep hierarchy, and pack it.
        const root = d3.pack()
            .size([this.width, this.height])
            .padding(3)
          (d3.hierarchy({children: I})
            .sum(i => V[i]))

        let leaf = this.svg.selectAll("a")
          .data(root.leaves())

        leaf.exit().remove()

        let leafEnter = leaf.enter()
          .append('a')
          .attr("transform", d => `translate(${d.x},${d.y})`)

        leafEnter.append("circle")
          .attr("fill", (d, i) => d3.schemeCategory10[i % 10])
          .attr("fill-opacity", 0.7)
          .attr("r", d => d.r)

        leafEnter.append("title")
          .text(d => T[d.data])

        // A unique identifier for clip paths (to avoid conflicts).
        const uid = `O-${Math.random().toString(16).slice(2)}`;

        leafEnter.append("clipPath")
            .attr("id", d => `${uid}-clip-${d.data}`)
          .append("circle")
            .attr("r", d => d.r);

        const tspan = leafEnter.append("text")
          .attr("clip-path", d => `url(${new URL(`#${uid}-clip-${d.data}`, location)})`)
          .selectAll("tspan")
          .data(d => `${L[d.data]}`.split(/ /g))

        tspan
          .enter()
          .append('tspan')
          .merge(tspan)
            .attr("x", 0)
            .attr("y", (d, i, D) => `${i - D.length / 2 + 0.85}em`)
            .attr("fill-opacity", (d, i, D) => i === D.length - 1 ? 0.7 : null)
            .text(d => d);
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
