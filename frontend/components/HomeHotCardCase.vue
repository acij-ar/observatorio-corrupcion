<template>
  <div v-if="cases" class="column is-3">
    <div class="hvrbox">
      <nuxt-link :to="{ name: 'expediente', query: { nombre: cases._key }}">
        <img
          :src="`https://raw.githubusercontent.com/acij-ar/observatorio-corrupcion/master/fotos/causas/${cases._key}.jpg`"
          :alt="`foto de la causa ${cases.nombre}`"
          class="hvrbox-layer_bottom"
        />
        <div class="hvrbox-layer_top">
          <div v-if="this.cases" class="hvrbox-text">{{ this.cases.nombre }}</div>
        </div>
      </nuxt-link>
    </div>
  </div>
</template>

<script>
import { HTTP } from '@/assets/utils'

export default {
  data () {
    return {
      cases: null
    }
  },
  props: {
    name: {
      type: String,
      require: true
    }
  },
  mounted: function () {
    this.getEntity()
  },
  methods: {
    getEntity: function () {
      HTTP.get(`nodo/nodos_causas/${this.name}?show=short`)
        .then(response => {
          this.cases = response.data.causa

          this.cases.foto = this.cases.nombre_causa != '' ? this.cases.link + '.jpg' : 'nn.png'
        })
    }
  }
}
</script>
