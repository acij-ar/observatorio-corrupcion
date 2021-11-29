<template>
  <section id="duracion" v-if="data.length !== 0">
    <div class="container">
      <base-buttons-share section="biografia" title="Duracion de las causas"
        plotName="duracionCausas"></base-buttons-share>

      <bar-stacked id="duracionCausas" :data="data"></bar-stacked>
    </div>
  </section>
</template>

<script>
import * as d3 from 'd3'
import BarStacked from '~/components/PlotBarStacked'
import BaseButtonsShare from '~/components/BaseButtonsShare'

export default {
  data () {
    return {
      data: []
    }
  },
  props: {
    magistrate: {
      type: Object,
      required: true
    }
  },
  components: {
    BarStacked,
    BaseButtonsShare
  },
  watch: {
    magistrate: function () {
      let data = []

      if (this.magistrate.histo_causas_abiertas.length !== 0) {
        data = [
          {name: 'abiertas',
          '≤ 3 años': this.magistrate.histo_causas_abiertas[0].value,
          '3 a 6 años': this.magistrate.histo_causas_abiertas[1].value,
          '6 a 10 años': this.magistrate.histo_causas_abiertas[2].value,
          '> 10 años': this.magistrate.histo_causas_abiertas[3].value,
          total: d3.sum(this.magistrate.histo_causas_abiertas, d => d.value)},
          {name: 'cerradas',
          '≤ 3 años': this.magistrate.histo_causas_cerradas[0].value,
          '3 a 6 años': this.magistrate.histo_causas_cerradas[1].value,
          '6 a 10 años': this.magistrate.histo_causas_cerradas[2].value,
          '> 10 años': this.magistrate.histo_causas_cerradas[3].value,
          total: d3.sum(this.magistrate.histo_causas_cerradas, d => d.value)}
        ]
        data.columns = ['name', '≤ 3 años', '3 a 6 años', '6 a 10 años', '> 10 años']
      }

      this.data = data
    }
  }
}
</script>
