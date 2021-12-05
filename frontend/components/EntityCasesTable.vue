<template>
  <section id="causas">
    <div class="container">
      <buttons-share
        :data="entity.causas"
        title="Causas de Corrupción"
        section="causas"
      />
    </div>
    <div class="container is-fluid">
      <p>
        La tabla se puede filtrar por nombre del expediente, juez/a, fiscal, delitos o denunciantes. 
      </p>

      <b-field grouped>
        <b-field>
          <b-input v-model="filterBy" placeholder="Filtrar por"></b-input>
        </b-field>

        <b-field>
          <b-select v-model="perPage">
            <option value="5">5 filas por página</option>
            <option value="10">10 filas por página</option>
            <option value="25">25 filas por página</option>
            <option value="50">50 filas por página</option>
          </b-select>
        </b-field>
      </b-field>

      <b-table
        :data="casesFilter"
        detailed
        :paginated=true
        :per-page="perPage"
        detail-key="expediente"
        @details-open="(row, index) => $buefy.toast.open(`Detalles caso ${row.expediente}`)"
        default-sort="anio_comienzo"
      >
        <b-table-column field="anio_comienzo" label="Año Comienzo" sortable v-slot="props">
          {{ props.row.anio_comienzo }}
        </b-table-column>

        <b-table-column field="expediente" label="Expediente" v-slot="props">
          <nuxt-link v-if="props.row.expediente"
          :to="{ name: 'expediente', query: { nombre: props.row._key }}">
            {{ props.row.nombre }}
          </nuxt-link>
        </b-table-column>

        <b-table-column field="juez" label="Juez/a" sortable v-slot="props">
          <nuxt-link v-if="props.row.juez"
          :to="{ name: 'magistrado', query: { nombre: props.row.juez.key }}">
            {{ props.row.juez.nombre }}
          </nuxt-link>
        </b-table-column>

        <b-table-column field="fiscal" label="Fiscal" sortable v-slot="props">
          <nuxt-link v-if="props.row.fiscal"
          :to="{ name: 'magistrado', query: { nombre: props.row.fiscal.key }}">
            {{ props.row.fiscal.nombre }}
          </nuxt-link>
        </b-table-column>

        <b-table-column field="delitos" label="Delitos" v-slot="props">
          <span v-for="delito in props.row.delitos" :key="delito.id">
            {{ delito }} --
          </span>
        </b-table-column>

        <b-table-column field="relacion" label="Relacion" sortable v-slot="props">
          {{ props.row.relacion.toUpperCase() }}
        </b-table-column>

        <b-table-column field="estado" label="Estado" sortable v-slot="props">
          {{ props.row.estado }}
        </b-table-column>

        <b-table-column field="denunciante" label="Denunciante" sortable v-slot="props">
          <span v-if="involved.relacion === 'denunciante'" v-for="involved in props.row.involucrados" :key="involved.id">
            <nuxt-link :to="{ name: 'entidad', query: { nombre: involved.key }}">
              {{ involved.nombre }} --
            </nuxt-link>
          </span>
        </b-table-column>

        <b-table-column field="querellante" label="Querellante" sortable v-slot="props">
          <div v-if="getQuerella(props.row.involucrados).length > 0">
            <span v-for="involved in getQuerella(props.row.involucrados)" :key="involved.id">
              <nuxt-link :to="{ name: 'entidad', query: { nombre: involved.key }}">
                {{ involved.nombre }} --
              </nuxt-link>
            </span>
          </div>
          <div v-else>
            <span>El CIJ no contiene información al respecto</span>
          </div>
        </b-table-column>

        <b-table-column field="ultima_actualizacion" label="Ultima Actualizacion" centered v-slot="props">
          <span v-if="props.row.ultima_actualizacion">
            {{ props.row.ultima_actualizacion }}
          </span>
          <span v-else>
            El CIJ no contiene información al respecto
          </span>
        </b-table-column>

        <b-table-column field="resuelve_texto" label="Resolucion" v-slot="props">
          <span @click="toggle(props.row)" class="aa">Ver investigados</span>
        </b-table-column>

        <template slot="detail" slot-scope="props">
          <div id="detailsTable">
            <b-table
              :data=props.row.involucrados
              :paginated=true
              :per-page=5
              default-sort="nombre"
              :row-class="(row, index) => ['juez', 'fiscal', 'denunciante'].includes(row.relacion) ? 'hidden-row' : ''"
            >
              <b-table-column field="nombre" label="Nombre" sortable v-slot="propsDetail">
                <nuxt-link :to="{ name: 'entidad', query: { nombre: propsDetail.row.key }}">
                  {{ propsDetail.row.nombre }}
                </nuxt-link>
              </b-table-column>

              <b-table-column field="relacion" label="Relacion" sortable v-slot="propsDetail">
                {{ propsDetail.row.relacion }}
              </b-table-column>
            </b-table>
          </div>
        </template>
      </b-table>

    </div><!--/.container -->
  </section><!--/.cases -->
</template>

<script>
import ButtonsShare from '@/components/BaseButtonsShare'

export default {
  data () {
    return {
      filterBy: '',
      perPage: 5,
      cases: [],
      casesFilter: []
    }
  },
  props: {
    entity: {
      type: Object,
      required: true
    }
  },
  components: {
    ButtonsShare
  },
  watch: {
    entity: function () {
      this.cases = this.entity.causas
      this.casesFilter = this.entity.causas
    },
    filterBy: function (filterBy) {
      /*
      Filtro la tabla por expediente, juez, fiscal, delitos y denunciantes
      */
      let regex = RegExp(filterBy, 'i')
      this.casesFilter = this.cases.filter(row => {
        let denunciantes = []
        row.involucrados.forEach(involved => {
          if (involved.relacion === 'denunciante') denunciantes.push(involved.nombre)
        })

        return regex.test(row.expediente) || regex.test(row.juez) || regex.test(row.fiscal)
          || regex.test(row.crimenes) || regex.test(denunciantes.join(' '))
      })
    }
  },
  methods: {
    getQuerella: function (involucrados) {
      return involucrados.filter(d => d.relacion === 'querellante')
    },
    toggle(row) {
      this.$refs.table.toggleDetails(row)
    }
  }
}
</script>

<style scoped>
#cases {
  padding-top: 80px;
  padding-bottom: 80px;
}

#cases header {
  padding-bottom: 50px;
}

.aa {
  color: blue;
  cursor: pointer;
}

#detailsTable {
  max-width: 90vw;
}
</style>
