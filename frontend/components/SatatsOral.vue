<template>
  <section id="juiciosOral" class="container">
    <buttons-share
      :data="data"
      title="Causas por juez/a"
      section="juiciosOral"
      plotName="judgesCount"
    />

    <p>
      Proporción de causas que llegan a juicio oral.
    </p>

    <bar-stacked
      v-if="data.length !== 0"
      id="juicioOral"
      :data="data"
      :height="600"
    />
  </section>
</template>

<script>
import * as d3 from 'd3'

import { apiUrl } from '@/assets/utils'
import BarStacked from '@/components/Charts/BarStacked'
import ButtonsShare from '@/components/BaseButtonsShare'

export default {
  data () {
    return {
      data: []
    }
  },
  components: {
    BarStacked,
    ButtonsShare,
  },
  mounted () {
    this.getData()
  },
  methods: {
    async getData() {
      const data = (await d3.json(`${apiUrl}estadisticas/jueces`))
        .resultado
        .map(d => ({
          name: d.juez.nombre,
          juicio_oral: d.juicio_oral,
          resto: d.total - d.juicio_oral,
          total: d.total
        }))

      data.sort((a, b) => b.total - a.total)
      data.columns = ['name', 'juicio_oral', 'resto']
      this.data = data
    }
  }
}
</script>
