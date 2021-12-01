<template>
  <section id="juiciosOral">
    <div class="container">
      <base-buttons-share section="juiciosOral" title="Causas por juez/a"
        :data="data" plotName="judgesCount"></base-buttons-share>

      <p>
        Proporcion de causas que llegan a juicio oral.
      </p>

      <bar-stacked v-if="data.length !== 0" id="juicioOral" :data="data"></bar-stacked>
    </div>
  </section>
</template>

<script>
import * as d3 from 'd3'
import { apiUrl } from '~/assets/utils'

import BarStacked from '~/components/PlotBarStacked'
import BaseButtonsShare from '~/components/BaseButtonsShare'

export default {
  data () {
    return {
      data: []
    }
  },
  components: {
    BarStacked,
    BaseButtonsShare
  },
  mounted () {
    this.getData()
  },
  methods: {
    getData: function () {
      d3.json(apiUrl + 'estadisticas/jueces')
        .then(dataJson => {
          let data = dataJson.resultado.map(d => ({
            name: d.juez.nombre,
            juicio_oral: d.juicio_oral,
            resto: d.total - d.juicio_oral,
            total: d.total
          }))

          data.sort((a, b) => b.total - a.total)
          data.columns = ['name', 'juicio_oral', 'resto']
          this.data = data
        })
    }
  }
}
</script>
