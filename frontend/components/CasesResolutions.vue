<template>
  <section id="resoluciones">
    <div class="container">
      <base-buttons-share section="resoluciones" title="Resoluciones" :data="cases.resoluciones"></base-buttons-share>

      <p v-if="Object.keys(cases).length === 0">
        El CIJ no contiene información al respecto
      </p>

      <b-table v-if="Object.keys(cases).length !== 0"
        :data="cases.resoluciones"
        ref="table"
        detailed
        detail-key="pdf_nombre"
        :paginated=true
        :per-page=5
        default-sort="fecha_resolucion"
        id="sentencias-table"
      >
        <b-table-column field="fecha_resolucion" label="Fecha resolucion" sortable v-slot="props">
          {{ props.row.fecha_resolucion.getDate() + '/' + props.row.fecha_resolucion.getMonth()
              + '/' + props.row.fecha_resolucion.getFullYear()  }}
        </b-table-column>

        <b-table-column field="camara" label="Camara" sortable v-slot="props">
          {{ props.row.camara }}
        </b-table-column>

        <b-table-column field="sala" label="Sala" v-slot="props">
          {{ props.row.sala }}
        </b-table-column>

        <b-table-column field="resuelve_texto" label="Resolucion" v-slot="props">
          {{ props.row.resuelve_texto.length > 300 ? props.row.resuelve_texto.slice(0, 300) + ' ... '
              : props.row.resuelve_texto }}
          <span v-if="props.row.resuelve_texto.length > 300" @click="toggle(props.row)" class="aa">[Leer mas]</span>
        </b-table-column>

        <b-table-column field="pdf_nombre" label="PDF" v-slot="props">
          <a :href="props.row.pdf_link" target="_blank">{{ props.row.pdf_nombre }}</a>
        </b-table-column>

        <template slot="detail" slot-scope="props">
          <p>{{ props.row.resuelve_texto }}</p>
        </template>
      </b-table>

    </div>
  </section>
</template>

<script>
import { baseUrl } from '~/assets/utils'
import BaseButtonsShare from '~/components/BaseButtonsShare'

export default {
  data () {
    return {
      baseUrl: baseUrl,
    }
  },
  props: {
    cases: {
      type: Object,
      required: true
    }
  },
  components: {
    BaseButtonsShare
  },
  methods: {
    toggle(row) {
      this.$refs.table.toggleDetails(row)
    }
  }
}
</script>

<style scoped>
.aa {
  color: blue;
  cursor: pointer;
}
</style>
