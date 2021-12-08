<template>
  <div v-if="magistrate" class="column is-3">
    <div class="hvrbox">
      <nuxt-link :to="{ name: 'magistrado', query: { nombre: magistrate._key }}">
        <img
          :src="`https://raw.githubusercontent.com/acij-ar/observatorio-corrupcion/master/fotos/magistrados/${magistrate.nombre}.jpg`"
          :alt="`foto del magistrado ${magistrate.nombre}`"
          class="hvrbox-layer_bottom"
        />
        <div class="hvrbox-layer_top">
          <div class="hvrbox-text">{{ this.magistrate.nombre }}</div>
        </div>
      </nuxt-link>
    </div>
  </div>
</template>

<script>
import { HTTP } from '~/assets/utils'

export default {
  data () {
    return {
      magistrate: null
    }
  },
  props: {
    name: {
      type: String,
      require: true
    }
  },
  mounted: function () {
    this.getData()
  },
  methods: {
    getData: function () {
      HTTP.get(`nodo/nodos_magistrados/${this.name}?show=short`)
        .then(response => {
          this.magistrate = response.data.magistrado
        })
    }
  }
}
</script>
