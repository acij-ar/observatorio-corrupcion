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

    <!-- Biography -->
    <entity-biography :entity="entity"></entity-biography>
    <!-- Stats -->
    <entity-stats :entity="entity"></entity-stats>
    <!-- A quien querella -->
    <entity-querella :entity="entity" v-if="entity.tipo === 'organismo estatal'"></entity-querella>
    <!-- Cases table -->
    <entity-cases-table :entity="entity"></entity-cases-table>

    <!-- Graph -->
    <graph></graph>
  </div>
</template>

<script>
import { getEntity } from '~/assets/utils'

import Graph from '~/components/BaseGraph'
import EntityBiography from '~/components/EntityBiography'
import EntityStats from '~/components/EntityStats'
import EntityQuerella from '~/components/EntityQuerella'
import EntityCasesTable from '~/components/EntityCasesTable'

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
    EntityBiography,
    EntityStats,
    EntityQuerella,
    EntityCasesTable
  },
  created () {
    this.getEntity()
  },
  beforeRouteUpdate (to, from, next) {
    window.scrollTo(0, 0)

    if (from.name === to.name) {
      next()
      this.getEntity()
    }

    next()
  },
  methods: {
    getEntity: getEntity
  }
}
</script>
