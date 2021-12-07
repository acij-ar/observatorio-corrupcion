<template>
  <section id="duracion" v-if="data.length !== 0">
    <div class="container">
      <base-buttons-share section="biografia" title="Duración de las causas"
        plotName="duracionCausas"></base-buttons-share>

      <div class="columns">
        <div class="column is-offset-2 is-8">
          <b-table :data="rows">
            <b-table-column field="label" label="Duración" v-slot="props">
              <div class="c">
                <div class="box" :style="{'background-color': colors[props.index]}"></div>
                {{ props.row.label }}
              </div>
            </b-table-column>

            <b-table-column field="close" label="Cantidad cerradas" v-slot="props">
              {{ props.row.close }}
            </b-table-column>

            <b-table-column field="open" label="Cantidad abiertas" v-slot="props">
              {{ props.row.open }}
            </b-table-column>
          </b-table>
        </div>
      </div>

      <bar-stacked id="duracionCausas" :data="data"></bar-stacked>
    </div>
  </section>
</template>

<script>
import * as d3 from 'd3'
import BarStacked from '~/components/Charts/BarStacked'
import BaseButtonsShare from '~/components/BaseButtonsShare'

export default {
  data () {
    return {
      data: [],
      rows: [],
      colors: d3.schemeCategory10,
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

        this.rows = [
          { label: '≤ 3 años', open: data[0]['≤ 3 años'], close: data[1]['≤ 3 años'] },
          { label: '3 a 6 años', open: data[0]['3 a 6 años'], close: data[1]['3 a 6 años'] },
          { label: '6 a 10 años', open: data[0]['6 a 10 años'], close: data[1]['6 a 10 años'] },
          { label: '> 10 años', open: data[0]['> 10 años'], close: data[1]['> 10 años'] },
        ]
      }

      this.data = data
    }
  }
}
</script>

<style scoped>
.c {
  display: inline-flex;
  align-items: center;
  gap: 10px;
}

.box {
  width: 50px;
  height: 30px;
}
</style>
