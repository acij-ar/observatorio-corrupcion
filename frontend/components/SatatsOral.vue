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
import { apiUrl, renameJudges } from '~/assets/utils'

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
    // Get initial data
    this.getData()
  },
  methods: {
    getData: function () {
      d3.json(apiUrl + 'estadisticas/jueces')
        .then(dataJson => {
          let dd = dataJson.resultado.map(d => {
            let name = Object.keys(renameJudges).includes(d.juez.nombre) ? renameJudges[d.juez.nombre]
              : d.juez.nombre

            return { name: name, juicio_oral: d.juicio_oral,
                     resto: d.total - d.juicio_oral, total: d.total }
          })

          dd.sort((a, b) => b.total - a.total)
          dd.columns = ['name', 'juicio_oral', 'resto']
          this.data = dd
        })
    }
  }
}
</script>
