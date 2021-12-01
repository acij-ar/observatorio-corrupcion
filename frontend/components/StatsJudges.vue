<template>
  <section id="jueces">
    <div class="container">
      <base-buttons-share section="jueces" title="Causas por juez/a"
        :data="data" plotName="judgesCount"></base-buttons-share>

      <p>
        Cantidad de casos de corrupcion abiertos por juez/a.
      </p>

      <bar id="judgeCount" :data="data"></bar>
    </div>
  </section>
</template>

<script>
import * as d3 from 'd3'
import { apiUrl } from '~/assets/utils'

import Bar from '~/components/PlotBar'
import BaseButtonsShare from '~/components/BaseButtonsShare'

export default {
  data () {
    return {
      data: []
    }
  },
  components: {
    Bar,
    BaseButtonsShare
  },
  mounted () {
    this.getData()
  },
  methods: {
    getData: function () {
      d3.json(apiUrl + 'estadisticas/jueces')
        .then(dataJson => {
          this.data = dataJson.resultado.map(d => ({ name: d.juez.nombre, value: d.total }))
          this.data.sort((a, b) => a.value - b.value )
        })
    }
  }
}
</script>
