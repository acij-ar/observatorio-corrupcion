<template>
  <section id="causasMasAntiguas">
    <div class="container">
      <base-buttons-share section="casosViejos" title="Causas abiertas mas antiguas"
        :data="cases"></base-buttons-share>

      <b-table :data="cases">
        <template slot-scope="props">
          <b-table-column field="index" label="Ranking">
              {{ props.index + 1 }}
          </b-table-column>

          <b-table-column field="anio_comienzo" label="Cantidad de años abierto">
              {{ new Date().getFullYear() - props.row.anio_comienzo }}
          </b-table-column>

          <b-table-column field="expediente" label="Expediente">
            <nuxt-link
            :to="{ name: 'expediente', query: { nombre: props.row._key }}">
              {{ props.row.nombre }}
            </nuxt-link>
          </b-table-column>

          <b-table-column field="caratula" label="Caratula">
              {{ props.row.caratula }}
          </b-table-column>
        </template>
      </b-table>

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
      cases: []
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
      d3.json(apiUrl + 'estadisticas/casos_viejos')
        .then(dataJson => this.cases = dataJson.resultado)
    }
  }
}
</script>
