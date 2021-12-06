<template>
  <section id="causasMasAntiguas" class="container">
    <buttons-share
      :data="cases"
      title="Causas abiertas más antiguas"
      section="casosViejos"
    />

    <b-table :data="cases">
      <b-table-column field="index" label="Ranking" v-slot="props">
        {{ props.index + 1 }}
      </b-table-column>

      <b-table-column field="anio_comienzo" label="Cantidad de años abierto" v-slot="props">
        {{ new Date().getFullYear() - props.row.anio_comienzo }}
      </b-table-column>

      <b-table-column field="expediente" label="Expediente" v-slot="props">
        <nuxt-link
        :to="{ name: 'expediente', query: { nombre: props.row._key }}">
          {{ props.row.nombre }}
        </nuxt-link>
      </b-table-column>

      <b-table-column field="caratula" label="Carátula" v-slot="props">
        {{ props.row.caratula }}
      </b-table-column>
    </b-table>
  </section>
</template>

<script>
import * as d3 from 'd3'

import { apiUrl } from '@/assets/utils'
import ButtonsShare from '@/components/BaseButtonsShare'

export default {
  data () {
    return {
      cases: []
    }
  },
  components: {
    ButtonsShare,
  },
  mounted () {
    this.getData()
  },
  methods: {
    async getData() {
      this.cases = (await d3.json(`${apiUrl}estadisticas/casos_viejos`)).resultado
    }
  }
}
</script>
