<template>
  <div>
    <section class="hero_secondary">
      <!-- Hero body -->
      <div class="hero-body">
        <div v-if="Object.keys(cases).length !== 0" class="container has-text-centered">
          <h1 class="title is-2">
            {{ this.cases.nombre }}
          </h1>

          <h2 v-if="cases.nombre !== cases.expediente" class="title is-3">
            {{ this.cases.expediente }}
          </h2>
        </div>
      </div>

      <!-- Hero footer -->
      <div class="hero-foot">
        <nav class="tabs">
          <div class="container">
            <ul>
              <li><a href="#descripcion">Descripcion</a></li>
              <li><a href="#involucrados">Involucrados</a></li>
              <li><a href="#resoluciones">Resoluciones</a></li>
              <li><a href="#conexiones">Conexiones</a></li>
            </ul>
          </div>
        </nav>
      </div>
    </section>

    <!-- Cases Description -->
    <cases-description :cases="cases"></cases-description>
    <!-- Cases involved -->
    <cases-involved :cases="cases"></cases-involved>
    <!-- -->
    <cases-resolutions :cases="cases"></cases-resolutions>
    <!-- Grafo -->
    <graph></graph>
  </div>
</template>

<script>
import { getCases } from '@/assets/utils'

import CasesDescription from '@/components/CasesDescription'
import CasesInvolved from '@/components/CasesInvolved'
import CasesResolutions from '@/components/CasesResolutions'
import Graph from '@/components/BaseGraph'

export default {
  head () {
    return {
      title: 'Expediente ' + this.$route.params.node
    }
  },
  data () {
    return {
      cases: {},

      // Page states
      isLoading: true,
      isError: false,
      errors: []
    }
  },
  components: {
    CasesDescription,
    CasesInvolved,
    CasesResolutions,

    Graph
  },
  created () {
    this.getCases()
  },
  beforeRouteUpdate (to, from, next) {
    window.scrollTo(0, 0)

    if (from.path === to.path) {
      next()
      this.getCase()
    }

    next()
  },
  methods: {
    getCases: getCases
  }
}
</script>

<style scoped>
.title.is-3 {
  color: white;
}
</style>
