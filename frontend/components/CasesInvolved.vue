<template>
  <section id="involucrados">
    <div v-if="Object.keys(cases).length !== 0" class="container">
      <base-buttons-share section="involucrados" title="Involucrados" :data="cases.involucrados"></base-buttons-share>

      <div class="block">
        <b-checkbox v-for="value in options" :key="value" v-model="checkBoxs" :native-value="value">
          {{ value }}
        </b-checkbox>
      </div>

      <b-table
        :data="data"
        :paginated=true
        :per-page=10
        default-sort="nombre">

        <template slot-scope="props">
          <b-table-column field="nombre" label="Nombre" sortable>
            <router-link :to="calcLink(props.row)">{{ props.row.nombre }}</router-link>
          </b-table-column>

          <b-table-column field="relacion" label="Relacion" sortable>
            {{ props.row.relacion }}
          </b-table-column>
        </template>
      </b-table>

    </div>
  </section>
</template>

<script>
import BaseButtonsShare from '@/components/BaseButtonsShare'

export default {
  data () {
    return {
      data: [],
      options: [],
      checkBoxs: []
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
  watch: {
    cases: function () {
      this.data = this.cases.involucrados
      this.options = Array.from(new Set(this.cases.involucrados.map(d => d.relacion)))
      this.checkBoxs = Array.from(new Set(this.cases.involucrados.map(d => d.relacion)))
    },
    checkBoxs: function () {
      this.data = this.cases.involucrados.filter(d => this.checkBoxs.includes(d.relacion))
    }
  },
  methods: {
    calcLink: function (row) {
      let name = ['juez', 'fiscal'].includes(row.relacion) ? 'magistrado'
        : 'entidad'

      return {
        name: name,
        query: { nombre: row.key }
      }
    }
  }
}
</script>
