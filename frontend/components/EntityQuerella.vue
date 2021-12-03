<template>
  <section id="querellante_de">
    <div v-if="entity.querellantes !== undefined" class="container">
      <base-buttons-share section="entidadQuerellante" title="Querellante"
        plotName="querellantePlot"></base-buttons-share>

      <p>
        Las {{ Math.min(this.entity.querellantes.length, 10) }} personas investigadas
        que mas aparecen en las causas donde la {{ this.entity.nombre }} es querellante.
      </p>
      <bar id="querellantePlot" :data="entity.querellantes"></bar>
    </div>
    <div v-else>
      <h2>Ésta entidad pública no es querellante en ninguna causa</h2>
    </div>
  </section>
</template>

<script>
import Bar from '~/components/Charts/Bar'
import BaseButtonsShare from '~/components/BaseButtonsShare'

export default {
  props: {
    entity: {
      type: Object,
      required: true
    }
  },
  components: {
    Bar,
    BaseButtonsShare
  }
}
</script>
