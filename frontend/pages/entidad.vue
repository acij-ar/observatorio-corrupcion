<template>
  <div>
    <portal to="header">
      <div class="hero-body">
        <h1 v-if="entity" class="title is-2">
          {{ this.entity.nombre }}
        </h1>
      </div>

      <div class="hero-footer">
        <nav class="tabs">
          <ul>
            <li><a href="#biografia">Biografia</a></li>
            <li><a href="#estadisticas">Estadisticas</a></li>
            <li><a href="#causas">Causas de corrupcion</a></li>
            <li><a href="#conexiones">Conexiones</a></li>
          </ul>
        </nav>
      </div>
    </portal>

    <entity-biography :entity="entity" />
    <entity-stats :entity="entity" />
    <entity-querella :entity="entity" v-if="entity.tipo === 'organismo estatal'" />
    <entity-cases-table :entity="entity" />
    <graph />
  </div>
</template>

<script>
import { getEntity } from '@/assets/utils'
import Graph from '@/components/BaseGraph'
import EntityStats from '@/components/EntityStats'
import EntityQuerella from '@/components/EntityQuerella'
import EntityBiography from '@/components/EntityBiography'
import EntityCasesTable from '@/components/EntityCasesTable'

export default {
  head () {
    return {
      title: this.entity.nombre ? this.entity.nombre : this.$route.query.nombre
    }
  },
  data () {
    return {
      entity: {},

      // Pages states
      isLoading: true,
      isError: false,
      errors: []
    }
  },
  components: {
    Graph,
    EntityStats,
    EntityQuerella,
    EntityBiography,
    EntityCasesTable,
  },
  created () {
    this.getEntity()
  },
  beforeRouteUpdate (to, from, next) {
    window.scrollTo(0, 0)

    if (from.name === to.name) {
      next()
      this.getEntity()
    } else {
      next()
    }
  },
  methods: {
    getEntity: getEntity
  }
}
</script>
