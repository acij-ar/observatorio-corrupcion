<template>
  <section id="casos">
    <div class="container">
      <base-buttons-share section="biografia" title="Causas relevantes"></base-buttons-share>

      <b-table
        v-if="magistrate.casos_importantes !== 0"
        id="tablaCasos"
        :data="magistrate.casos_importantes"
        :paginated=true
        :per-page="perPage"
        default-sort="anio_comienzo"
      >
        <b-table-column field="anio_comienzo" label="Año Comienzo" sortable v-slot="props">
          {{ props.row.anio_comienzo }}
        </b-table-column>

        <b-table-column field="expediente" label="Expediente" v-slot="props">
          <nuxt-link :to="{ name: 'expediente', query: { nombre: props.row.key }}">
            {{ props.row.nombre }}
          </nuxt-link>
        </b-table-column>

        <b-table-column field="fiscal" label="Fiscal" sortable v-slot="props">
          <nuxt-link :to="{ name: 'magistrado', query: { nombre: props.row.fiscal.key }}">
            {{ props.row.fiscal.nombre }}
          </nuxt-link>
        </b-table-column>

        <b-table-column field="denunciante" label="Denunciante" sortable v-slot="props">
          <span v-for="involved in props.row.denunciantes" :key="involved.id">
            <nuxt-link :to="{ name: 'entidad', query: { nombre: involved }}">
              {{ involved.replace(/_/g, ' ') }} --
            </nuxt-link>
          </span>
        </b-table-column>

        <b-table-column field="querellante" label="Querellante" sortable v-slot="props">
          <span v-for="involved in props.row.querellantes" :key="involved.id">
            <nuxt-link :to="{ name: 'entidad', query: { nombre: involved }}">
              {{ involved.replace(/_/g, ' ') }} --
            </nuxt-link>
          </span>
        </b-table-column>

        <b-table-column field="estado" label="Estado" sortable v-slot="props">
          {{ props.row.estado }}
        </b-table-column>

        <b-table-column field="ultima_actualizacion" label="Ultima Actualización" centered v-slot="props">
          {{ props.row.ultima_actualizacion }}
        </b-table-column>
      </b-table>
    </div>
  </section>
</template>

<script>
import BaseButtonsShare from '~/components/BaseButtonsShare'

// casos_importantes

export default {
  data () {
    return {
      perPage: 5
    }
  },
  props: {
    magistrate: {
      type: Object,
      required: true
    }
  },
  components: {
    BaseButtonsShare
  }
}
</script>
