<template>
  <section id="casosPorAnio">
    <div class="container">
      <base-buttons-share section="casosPorAnio" title="Causas por año"
        :data="data" plotName="casesByYear"></base-buttons-share>

      <p>
        Cantidad de causas de corrupcion segun el año de comienzo desde el 2013.
      </p>

      <bar-vertical id="casesByYear" :data="data"></bar-vertical>
    </div>
  </section>
</template>

<script>
import * as d3 from 'd3'
import { apiUrl } from '@/assets/utils'
import BarVertical from '~/components/PlotBarVertical'
import BaseButtonsShare from '~/components/BaseButtonsShare'

export default {
  data () {
    return {
      data: []
    }
  },
  components: {
    BarVertical,
    BaseButtonsShare
  },
  mounted () {
    // Get initial data
    this.getData()
  },
  methods: {
    getData: function () {
      d3.json(apiUrl + 'estadisticas/casos_por_anio')
        .then(dataJson => {
          this.data = dataJson.resultado

          this.data.sort((a, b) => a.name - b.name)
          this.data = this.data.filter(d => parseInt(d.name) >= 2013)
        })
    }
  }
}
</script>
