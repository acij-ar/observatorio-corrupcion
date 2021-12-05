<template>
  <section id="topPorRelacion" class="container">
    <buttons-share
      :data="data"
      title="Personas más"
      section="topRelacion"
      plotName="relations"
    >
      <b-field class="is-inline-block">
          <b-select placeholder="Selecciona una metrica" v-model="selectedMetric">
            <option
              v-for="option in metrics"
              :value="option.value"
              :key="option.id">
              {{ option.text }}
            </option>
          </b-select>
      </b-field>
    </buttons-share>

    <bar id="topRelacion" :data="data" />
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
      data: [],
      selectedMetric: 'denunciante',
      metrics: [
        { value: 'denunciante', text: 'denunciantes' },
        { value: 'querellante', text: 'querellantes' },
        { value: 'investigado', text: 'investigadas' },
      ]
    }
  },
  components: {
    Bar,
    ButtonsShare,
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
    async getData (metric) {
      const data = await d3.json(`${apiUrl}estadisticas/top_relacion/${metric}`)
      this.data = data.resultado.map(d => ({
        name: d.nombre,
        value: d.cantidad,
      }))
    }
  }
}
</script>
