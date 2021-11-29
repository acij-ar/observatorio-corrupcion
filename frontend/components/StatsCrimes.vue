<template>
  <section id="crimenes">
    <div class="container">
      <base-buttons-share section="crimenes" title="Top de delitos"
        :data="data" plotName="topCrimes"></base-buttons-share>

      <base-bubble-plot v-if="data.length > 0" id="delitos" :data="data"></base-bubble-plot>
    </div>
  </section>
</template>

<script>
import * as d3 from 'd3'
import { apiUrl } from '@/assets/utils'
import BaseBubblePlot from '~/components/BaseBubblePlot'
import BaseButtonsShare from '~/components/BaseButtonsShare'

export default {
  data () {
    return {
      data: []
    }
  },
  components: {
    BaseBubblePlot,
    BaseButtonsShare
  },
  mounted () {
    this.getData()
  },
  methods: {
    getData: function () {
      d3.json(apiUrl + 'estadisticas/delitos')
        .then(dataJson => {
          this.data = dataJson.resultado.map(d => {
            return { name: d.crimen, value: d.cantidad }
          })
        })
    }
  }
}
</script>
