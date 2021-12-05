<template>
  <section id="jueces" class="container">
    <buttons-share
      :data="data"
      title="Causas por juez/a"
      section="jueces"
      plotName="judgesCount"
    />

    <p>
      Cantidad de casos de corrupción abiertos por juez/a.
    </p>

    <bar id="judgeCount" :data="data" :height="600" />
  </section>
</template>

<script>
import * as d3 from 'd3'

import { apiUrl } from '@/assets/utils'
import Bar from '@/components/Charts/Bar'
import ButtonsShare from '@/components/BaseButtonsShare'

export default {
  data () {
    return {
      data: []
    }
  },
  components: {
    Bar,
    ButtonsShare,
  },
  mounted () {
    this.getData()
  },
  methods: {
    async getData() {
      this.data = (await d3.json(`${apiUrl}estadisticas/jueces`))
        .resultado
        .map(d => ({ name: d.juez.nombre, value: d.total }))
      this.data.sort((a, b) => a.value - b.value )
    }
  }
}
</script>
