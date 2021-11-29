<template>
  <div>
    <section class="hero_secondary">
      <!-- Hero body -->
      <div class="hero-body">
        <div class="container has-text-centered">
          <h1 v-if="magistrate" class="title is-2">
            {{ this.magistrate.nombre }}
          </h1>

          <h2 v-if="magistrate" class="title is-3">
            {{ this.magistrate.subtipo }}
          </h2>
        </div>
      </div>

      <!-- Hero footer -->
      <div class="hero-foot">
        <nav class="tabs">
          <div class="container">
            <ul>
              <li><a href="#biografia">Biografia</a></li>
              <li><a href="#casos">Causas importante</a></li>
              <li><a href="#investigados">Mas investigados</a></li>
              <li><a href="#duracion">Duracion de las causas</a></li>
            </ul>
          </div>
        </nav>
      </div>
    </section>

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
