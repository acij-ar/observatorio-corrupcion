<template>
  <div v-if="entity" class="column is-3">
    <div class="hvrbox">
      <nuxt-link :to="{ name: 'entidad', query: { nombre: entity._key }}">
        <img
          :src="`https://raw.githubusercontent.com/acij-ar/observatorio-corrupcion/master/fotos/entidades/${entity.foto}`"
          :alt="`foto de ${entity.nombre}`"
          class="hvrbox-layer_bottom"
        />
        <div class="hvrbox-layer_top">
          <div class="hvrbox-text">{{ this.entity.nombre }}</div>
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
      entity: null
    }
  },
  props: {
    name: {
      type: String,
      require: true
    }
  },
  mounted: function () {
    this.getCase()
  },
  methods: {
    getCase: function () {
      HTTP.get(`nodo/nodos_entidades/${this.name}?show=short`)
        .then(response => {
          this.entity = response.data.entidad

          if (this.entity.foto === '') {
            this.entity.foto = 'nn.png'
          }
        })
    }
  }
}
</script>
