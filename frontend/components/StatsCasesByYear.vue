<template>
  <section id="casosPorAnio" class="container">
      <buttons-share
        :data="data"
        title="Causas por año"
        section="casosPorAnio"
        plotName="casesByYear"
      />

      <p>
        Cantidad de causas de corrupcion segun el año de comienzo desde el 2013.
      </p>

      <bar-vertical id="casesByYear" :data="data" yLabel="" />
  </section>
</template>

<script>
import * as d3 from 'd3'

import { apiUrl } from '@/assets/utils'
import BarVertical from '@/components/Charts/BarVertical'
import ButtonsShare from '@/components/BaseButtonsShare'

export default {
  data () {
    return {
      data: []
    }
  },
  components: {
    BarVertical,
    ButtonsShare,
  },
  mounted () {
    this.getData()
  },
  methods: {
    async getData() {
      this.data = (await d3.json(`${apiUrl}/estadisticas/casos_por_anio`)).resultado
      this.data.sort((a, b) => a.name - b.name)
      this.data = this.data.filter(d => parseInt(d.name) >= 2013)
    }
  }
}
</script>
