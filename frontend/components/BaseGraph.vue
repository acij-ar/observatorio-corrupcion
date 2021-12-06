<template>
  <section id="conexiones" class="container pb-6">
      <buttons-share
        v-if="graph !== null"
        :data="graph.links"
        title="Conexiones"
        section="conexiones"
        plotName="chart"
      />

      <p>
        Hacé doble click sobre el nodo para visitar el perfil correspondiente.
      </p>

      <svg id="chart" />
  </section>
</template>

<script>
import * as d3 from 'd3'

import { apiUrl } from '@/assets/utils'
import ButtonsShare from '@/components/BaseButtonsShare'

export default {
  props: {
    width: {
      type: Number,
      default: 1600,
    },
    height: {
      type: Number,
      default: 800,
    },
    margin: {
      type: Object,
      default: () => ({ top: 20, right: 20, bottom: 20, left: 20 })
    },
  },
  data () {
    return {
      svg: null,

      // Graph data
      zoom: null,
      simulation: null,
      graph: null,
      link: null,
      node: null,
      linkedByIndex: {},
      mainNodes: [],
    }
  },
  components: {
    ButtonsShare,
  },
  mounted () {
    this.svg = d3.select('#chart')
      .attr("width", this.width)
      .attr("height", this.height)
      .attr("viewBox", [0, 0, this.width, this.height])
      .attr("style", "max-width: 100%; height: auto; height: intrinsic;")

    this.svg
      .append('g')
      .attr('class', 'zoom')

    this.svg.select('.zoom')
      .append('g')
      .attr('class', 'links')

    this.svg.select('.zoom')
      .append("g")
      .attr("class", "nodes")

    let colors = {
      'expediente judicial': '#e41a1c',
      'persona': '#377eb8',
      'fiscal': '#4daf4a',
      'juez': '#984ea3',
      'organismo estatal': '#ff7f00'
    }

    let name = this.$route.query.nombre.replace(/_/g, ' ')
    colors[name] = '#06b4ab'

    // Append legend
    this.svg.append('g')
      .attr('class', 'labels')
      .attr('transform', 'translate(20, 20)')
      .append('rect')

    let legend = this.svg.select('.labels')
      .selectAll('.legend')
      .data(Object.keys(colors))
      .enter().append('g')
      .attr('class', 'legend')
      .attr('transform', (d, i) => `translate(0,${10 + i * 25})`)
      .attr('cursor', 'pointer')
      .on('click', d => { console.log(d) })

    legend.append('circle')
      .attr('r', 7)
      .attr('cx', this.width - 120)
      .attr('cy', 10)
      .style('fill', d => colors[d])

    legend.append('text')
      .attr('x', this.width - 120 - 24)
      .attr('y', 9)
      .attr('dy', '.35em')
      .style('text-anchor', 'end')
      .text(d => d)

    // Legend background rect
    let bbox
    this.svg.select('.labels')
      .each(function(d) { bbox = [this.getBBox()] })
      .data(bbox)
      .select('rect')
      .attr('x', d => d.x - 30)
      .attr('y', d => 2)
      .attr('width', d => d.width + 50)
      .attr('height', d => d.height + 20)

    // Add zoom capabilities
    this.zoom = d3.zoom()
      .on('zoom', zoom_actions)

    this.zoom(this.svg)

    // Zoom functions
    let that = this
    function zoom_actions() {
      that.svg
        .select('.zoom')
        .attr('transform', d3.event.transform)
    }

    this.getData()
  },
  watch: {
    '$route.query' (to, from) {
      this.getData()
    },
    graph: function () {
      // "Reset" the graph
      this.zoom.transform(this.svg, d3.zoomIdentity)
      this.svg.select('.links').selectAll('line').remove()
      this.svg.select('.nodes').selectAll('g').remove()

      let top = parseInt(10 * this.graph.nodes.length / 100)
      top = top > 30 ? 30 : top

      this.mainNodes = this.graph.nodes
        .filter(d => !d.nombre.startsWith('CFP'))
        .sort((a, b) => b.metricas.degree - a.metricas.degree)
        .map(d => d.id)
        .slice(0, top)

      // Set the radio of the node bettwen [5, 23] using sqrt function
      let radioScale = d3.scaleSqrt()
        .range([5, 23])
        .domain([
          d3.min(this.graph.nodes, (d) => d.metricas.degree),
          d3.max(this.graph.nodes, (d) => d.metricas.degree)
        ])

      // Start the simulation
      this.simulation = d3.forceSimulation()
        .force('link', d3.forceLink().id(d => d.id))
        .force('charge', d3.forceManyBody().strength(-100))
        .force('center', d3.forceCenter(this.width / 2, this.height / 2))
        .force('collide', d3.forceCollide().radius(d => 2 * radioScale(d.metricas.degree)))

      this.link = this.svg.select('.links')
        .selectAll('line')
        .data(this.graph.links)
        .enter()
        .append('line')
        .attr('stroke-width', 4)

      this.node = this.svg.select('.nodes')
        .selectAll("g")
        .data(this.graph.nodes)
        .enter()
        .append("g")

      let circles = this.node.append("circle")
        .attr('r', d => radioScale(d.metricas.degree))
        .attr('fill', d => this.color(d))
        .on('mouseover', d => this.mouseover(d))
        .on('mouseout', d => this.mouseout(d))
        .on('dblclick', d => this.goToNode(d))
        .call(d3.drag()
          .on('start', this.dragstarted)
          .on('drag', this.dragged)
          .on('end', this.dragended))

      let labels = this.node.append("text")
        .text(d => this.showLabel(d))
        .attr('x', d => radioScale(d.metricas.degree))
        .attr('y', d => 5)
        .call(getBB)

      // Rect to give label background color
      this.node.insert("rect", "text")
        .attr("x", d => d.bbox.x)
        .attr("y", d => d.bbox.y)
        .attr("width", d => d.bbox.width)
        .attr("height", d => d.bbox.height)
        .style("fill", "yellow")

      function getBB(selection) {
        selection.each(function(d) { d.bbox = this.getBBox(); })
      }

      this.simulation
        .nodes(this.graph.nodes)
        .on('tick', this.ticked)

      this.simulation
        .force('link')
        .links(this.graph.links)

      // Calculate matrix of connectios
      this.graph.links.forEach(d => {
        this.linkedByIndex[d.source.index + ',' + d.target.index] = 1
      })
    }
  },
  methods: {
    getData () {
      let collection = this.$route.name === 'entidad' ? 'nodos_entidades/'
      : this.$route.name === 'expediente' ? 'nodos_causas/'
        : this.$route.name === 'magistrado' ? 'nodos_magistrados/'
          : ''

      // En el caso de que sea dentro de embeber obtengo la
      // colleccion en base al query parameter
      if (this.$route.path === '/embeber') {
        let area = this.$route.query.area

        collection = area === 'entidad' ? 'nodos_entidades/'
          : area === 'expediente' ? 'nodos_causas/'
            : area === 'magistrado' ? 'nodos_magistrados/'
              : ''
      }

      // Get the data
      const url = apiUrl + 'grafo/' + collection + this.$route.query.nombre + '?profundidad=2'
      d3.json(url)
        .then(data => { this.graph = data.grafo })
    },
    color: function (d) {
      let nodeType = d.tipo === 'magistrado' ? d.subtipo
        : ['persona', 'empresa', 'entidad', 'ong'].includes(d.tipo) ? 'entidad'
          : d.tipo

      let color = nodeType === 'expediente judicial' ? '#e41a1c'
        : nodeType === 'organismo estatal' ? '#ff7f00'
          : nodeType === 'entidad' ? '#377eb8'
            : nodeType === 'fiscal' ? '#4daf4a'
              : nodeType === 'juez' ? '#984ea3'
                  : 'black'

      if (d.id.split('/')[1] === this.$route.query.nombre){
        color = '#06b4ab'
      }

      return color
    },
    showLabel: function (node) {
      if (this.mainNodes.includes(node.id)) {
        return node.nombre
      } else {
        return ''
      }
    },
    ticked: function () {
      this.link
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y)

      this.node
        .attr("transform", d => `translate(${d.x}, ${d.y})`)
    },
    dragstarted: function (d) {
      if (!d3.event.active) this.simulation.alphaTarget(0.3).restart()
      d.fx = d.x
      d.fy = d.y
    },
    dragged: function (d) {
      d.fx = d3.event.x
      d.fy = d3.event.y
    },
    dragended: function (d) {
      if (!d3.event.active) this.simulation.alphaTarget(0)
      d.fx = null
      d.fy = null
    },
    mouseover: function (d) {
      /*
        On mouse over highlight the rect and shoe the tooltip
      */
      this.link
        .transition(500)
        .style('stroke-opacity', o => { return o.source === d || o.target === d ? 1 : 0.2 })

      this.node
        .transition(500)
        .style('opacity', o => { return this.isConnected(o, d) ? 1.0 : 0.2 })

      // Update the tooltip position and value
      d3.select('#tooltip')
        .style('left', (d3.event.pageX - 125) + 'px')
        .style('top', (d3.event.pageY + 20) + 'px')
        .select('#value')
        .html(() => {
          let nodeType
          if (d.tipo === 'magistrado') {
            nodeType = d.subtipo
          } else {
            nodeType = d.tipo
          }
          let etiqueta = d.nombre+"<br>"+"Hace doble click para acceder a más información sobre la persona, institución pública o causa";
          return nodeType === 'expediente judicial' ? 'Expediente Judicial: ' + etiqueta
            : nodeType === 'entidad' ? 'Involucrado: ' + etiqueta
              : nodeType === 'fiscal' ? 'Fiscal: ' + etiqueta
                : nodeType === 'juez' ? 'Juez: ' + etiqueta
                  : etiqueta
        })

      // Show the tooltip
      d3.select('#tooltip').classed('hidden', false)
    },
    mouseout: function (d) {
      /*
        On mouse out, remove the highlight
      */
      this.link
        .transition(500)
        .style('stroke-opacity', 1)

      this.node
        .transition(500)
        .style('opacity', 1)

      d3.select('#tooltip').classed('hidden', true)
    },
    goToNode: function (node) {
      let typeNode = node.id.split('/')[0]
      let nodeName = node.id.split('/')[1]

      let name = typeNode === 'nodos_entidades' ? 'entidad'
        : typeNode === 'nodos_causas' ? 'expediente'
          : typeNode === 'nodos_magistrados' ? 'magistrado'
            : ''

      this.$router.push({ name: name, query: { nombre: nodeName }})
    },
    isConnected: function (a, b) {
      /*
        Return true if two nodes are connected
      */
      return this.linkedByIndex[a.index + ',' + b.index] ||
             this.linkedByIndex[b.index + ',' + a.index] ||
             a.index === b.index
    }
  }
}
</script>
