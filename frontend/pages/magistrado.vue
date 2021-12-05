<template>
  <div>
    <portal to="header">
      <div class="hero-body">
        <h1 v-if="magistrate" class="title is-2">
          {{ this.magistrate.nombre }}
        </h1>

        <h2 v-if="magistrate" class="title is-3">
          {{ this.magistrate.subtipo }}
        </h2>
      </div>

      <!-- Hero footer -->
      <div class="hero-footer">
        <nav class="tabs">
          <ul>
            <li><a href="#biografia">Biografia</a></li>
            <li><a href="#casos">Causas importante</a></li>
            <li><a href="#investigados">Más investigados/as</a></li>
            <li><a href="#duracion">Duración de las causas</a></li>
          </ul>
        </nav>
      </div>
    </portal>

    <magistrate-biography :magistrate="magistrate"></magistrate-biography>
    <magistrate-cases :magistrate="magistrate"></magistrate-cases>
    <magistrate-most-invest :magistrate="magistrate"></magistrate-most-invest>
    <magistrate-cases-duration :magistrate="magistrate"></magistrate-cases-duration>
  </div>
</template>

<script>
import { getMagistrate } from '@/assets/utils'
import MagistrateBiography from '~/components/MagistrateBiography'
import MagistrateCases from '~/components/MagistrateCases'
import MagistrateMostInvest from '~/components/MagistrateMostInvest'
import MagistrateCasesDuration from '~/components/MagistrateCasesDuration'
import Graph from '~/components/BaseGraph'

export default {
  head () {
    return {
      title: this.$route.params.node
    }
  },
  data () {
    return {
      magistrate: {}
    }
  },
  components: {
    MagistrateBiography,
    MagistrateCases,
    MagistrateMostInvest,
    MagistrateCasesDuration,
    Graph
  },
  created () {
    this.getMagistrate()
  },
  beforeRouteUpdate (to, from, next) {
    window.scrollTo(0, 0)

    if (from.path === to.path) {
      next()
      this.getMagistrate()
    }

    next()
  },
  methods: {
    getMagistrate: getMagistrate
  }
}
</script>


<style scoped>
.title.is-3 {
  color: white;
}
</style>
