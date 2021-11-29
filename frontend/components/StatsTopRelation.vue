<template>
  <section id="topPorRelacion">
    <div class="container">
      <base-buttons-share section="topRelacion" title="Personas mas"
        :data="data" plotName="relations">

        <b-field class="l">
            <b-select placeholder="Selecciona una metrica" v-model="selectedMetric">
                <option
                    v-for="option in metrics"
                    :value="option.value"
                    :key="option.id">
                    {{ option.text }}
                </option>
            </b-select>
        </b-field>

      </base-buttons-share>

      <bar id="topRelacion" :data="data"></bar>
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
      data: [],

      selectedMetric: 'denunciante',
      metrics: [{ value: 'denunciante', text: 'denunciantes' },
                { value: 'querellante', text: 'querellantes' },
                { value: 'investigado', text: 'investigadas' }]
    }
  },
  components: {
    Bar,
    BaseButtonsShare
  },
  mounted () {
    this.getData(this.selectedMetric)
  },
  watch: {
    selectedMetric: function () {
      this.getData(this.selectedMetric)
    }
  },
  methods: {
    getData: function (metric) {
      this.data = []

      d3.json(apiUrl + 'estadisticas/top_relacion/' + metric)
        .then(dataJson => {
          this.data = dataJson.resultado.map(d => {
            return {
              name: d.nombre,
              value: d.cantidad
            }
          })
        })
    }
  }
}
</script>

<style scoped>
.l {
  display: inline-block;
}
</style>
