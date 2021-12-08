<template>
  <section id="descripcion">
    <div v-if="Object.keys(cases).length !== 0" class="container">
      <base-buttons-share section="resumen" title="Descripción"></base-buttons-share>

      <div class="columns is-tablet">
        <div class="column is-5">
          <figure class="image">
            <img
              :src="`https://raw.githubusercontent.com/acij-ar/observatorio-corrupcion/master/fotos/causas/${cases._key}.jpg`"
              :alt="`foto de la causa ${cases.nombre}`"
            />
          </figure>
          <p style="font-size: 0.9rem;">
            Fuente de la foto: {{ this.cases.fuente_foto }}
          </p>
        </div>

        <div class="column is-6 s">
          <p>
            <span class="title is-5">Carátula:</span> {{ this.cases.caratula }}
          </p>

          <p>
            <span class="title is-5">Fecha de comienzo:</span> {{ this.cases.anio_comienzo }}
          </p>

          <p>
            <span class="title is-5">Estado actual:</span> {{ this.cases.estado }}
          </p>
        </div><!--/column -->
      </div><!--/columns -->

      <p>{{ this.cases.hechos }}</p>

    </div><!--/container -->
  </section>
</template>

<script>
import BaseButtonsShare from '~/components/BaseButtonsShare'

export default {
  props: {
    cases: {
      type: Object,
      required: true
    }
  },
  components: {
    BaseButtonsShare
  },
}
</script>

<style scoped>
.s {
  padding-top: 20px;
}

.s p {
  padding-bottom: 20px;
}
</style>
