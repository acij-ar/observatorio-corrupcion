<template>
  <div>
    <section class="hero_secondary">
      <!-- Hero body -->
      <div class="hero-body">
        <div class="container has-text-centered">
          <h1 class="title">
            {{ name }}
          </h1>
        </div>
      </div>
    </section>

    <graph v-if="section === 'conexiones'"></graph>

    <!-- Entity -->
    <entity-biography v-else-if="area === 'entidad' && section === 'biografia'" :entity="entity"></entity-biography>
    <entity-stats v-else-if="area === 'entidad' && section === 'estadisticas'" :entity="entity"></entity-stats>
    <entity-cases-table v-else-if="area === 'entidad' && section === 'causas'" :entity="entity"></entity-cases-table>

    <!-- Cases -->
    <cases-description v-else-if="area === 'expediente' && section === 'resumen'" :cases="cases"></cases-description>
    <cases-involved v-else-if="area === 'expediente' && section === 'involucrados'" :cases="cases"></cases-involved>
    <cases-resolutions v-else-if="area === 'expediente' && section === 'resoluciones'" :cases="cases"></cases-resolutions>

    <!-- Stats -->
    <stats-top-relation v-else-if="area === 'estadisticas' && section === 'topRelacion'"></stats-top-relation>
    <stats-cases-by-year v-else-if="area === 'estadisticas' && section === 'casosPorAnio'"></stats-cases-by-year>
    <stats-judges v-else-if="area === 'estadisticas' && section === 'jueces'"></stats-judges>
    <stats-oral v-else-if="area === 'estadisticas' && section === 'juiciosOral'"></stats-oral>
    <stats-crimes v-else-if="area === 'estadisticas' && section === 'crimenes'"></stats-crimes>
    <stats-old-cases v-else-if="area === 'estadisticas' && section === 'casosViejos'"></stats-old-cases>
    <stats-duration v-else-if="area === 'estadisticas' && section === 'duracionCausas'"></stats-duration>

    <div v-else>
      <p>
        Le erraste pibe
      </p>
    </div>

  </div>
</template>

<script>
import { getEntity, getCases } from '@/assets/utils'

import Graph from '~/components/BaseGraph'

import EntityBiography from '~/components/EntityBiography'
import EntityStats from '~/components/EntityStats'
import EntityCasesTable from '~/components/EntityCasesTable'

import CasesDescription from '~/components/CasesDescription'
import CasesInvolved from '~/components/CasesInvolved'
import CasesResolutions from '~/components/CasesResolutions'

import StatsTopRelation from '~/components/StatsTopRelation'
import StatsCasesByYear from '~/components/StatsCasesByYear'
import StatsJudges from '~/components/StatsJudges'
import StatsOral from '~/components/SatatsOral'
import StatsCrimes from '~/components/StatsCrimes'
import StatsOldCases from '~/components/StatsOldCases'
import StatsDuration from '~/components/StatsDuration'

export default {
  // head () {
  //   return {
  //     title: this.$route.params.node
  //   }
  // },
  data () {
    return {
      entity: {},
      cases: {},

      // Page states
      isLoading: true,
      isError: false,
      errors: [],

      //
      name: null,
      area: null,
      section: null
    }
  },
  components: {
    Graph,

    // Entity components
    EntityBiography,
    EntityStats,
    EntityCasesTable,

    // Cases components
    CasesDescription,
    CasesInvolved,
    CasesResolutions,

    // Stats
    StatsTopRelation,
    StatsCasesByYear,
    StatsJudges,
    StatsOral,
    StatsCrimes,
    StatsOldCases,
    StatsDuration
  },
  watch: {
    entity: function () {
      this.name = this.entity.nombre
    },
    cases: function () {
      this.name = 'Causa: ' + this.cases.nombre
    }
  },
  created () {
    this.area = 'area' in this.$route.query ? this.$route.query.area : ''
    this.section = 'section' in this.$route.query ? this.$route.query.section : ''

    if (this.area === 'entidad') {
      this.getEntity()
    }
    else if (this.area === 'expediente') {
      this.getCases()
    }
  },
  methods: {
    getEntity: getEntity,
    getCases: getCases
  }
}
</script>

<style scoped>
.hero-body {
  padding-top: 2rem;
}
</style>
