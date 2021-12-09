<template>
  <section id="crimenes" class="container">
    <buttons-share
      :data="data"
      title="Top de delitos"
      section="crimenes"
      plotName="delitos"
    />
    <p>Posando el mouse sobre cada círculo podes ver a qué delito corresponde</p>
    <bubble v-if="data.length > 0" id="delitos" :data="data" />
  </section>
</template>

<script>
import * as d3 from 'd3'

import { apiUrl } from '@/assets/utils'
import Bubble from '@/components/Charts/Bubble'
import ButtonsShare from '@/components/BaseButtonsShare'

export default {
  data () {
    return {
      data: []
    }
  },
  components: {
    Bubble,
    ButtonsShare,
  },
  mounted () {
    this.getData()
  },
  methods: {
    async getData() {
      this.data = (await d3.json(`${apiUrl}estadisticas/delitos`))
        .resultado
        .map(d => ({ name: d.crimen, value: d.cantidad }))
    }
  }
}
</script>
