<template>
  <section id="main" class="has-text-centered">
    <!-- Entidades -->
    <div v-if="entities.length > 0" class="container">
      <h2 class="title is-2">Personas destacadas</h2>

      <div class="columns">
        <card-entity
          v-for="entitieName in entities"
          :key="entitieName"
          :name="entitieName"
        />
      </div>
    </div>

    <!-- Causas -->
    <div v-if="cases.length > 0" class="container">
      <h2 class="title is-2">Causas relevantes</h2>

      <div class="columns">
        <card-case
          v-for="caseName in cases"
          :key="caseName"
          :name="caseName"
        />
      </div>
    </div>

    <!-- Magistrados -->
    <div v-if="magistrates.length > 0" class="container">
      <h2 class="title is-2">Juezas/ces y Fiscales</h2>

      <div class="columns">
        <card-magistrate
          v-for="magistrateName in magistrates"
          :key="magistrateName"
          :name="magistrateName"
        />
      </div>
    </div>
  </section>
</template>

<script>
import * as d3 from 'd3'
import CardCase from '@/components/HomeHotCardCase'
import CardEntity from '@/components/HomeHotCardEntity'
import CardMagistrate from '@/components/HomeHotCardMagistrate'

export default {
  data () {
    return {
      entities: [],
      cases: [],
      magistrates: []
    }
  },
  components: {
    CardCase,
    CardEntity,
    CardMagistrate
  },
  mounted () {
    this.getHotCases()
    this.getHotEntities()
    this.getHotMagistrates()
  },
  methods: {
    shuffle(array) {
      let currentIndex = array.length,  randomIndex

      // While there remain elements to shuffle...
      while (currentIndex != 0) {

        // Pick a remaining element...
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex--;

        // And swap it with the current element.
        [array[currentIndex], array[randomIndex]] = [
          array[randomIndex], array[currentIndex]];
      }

      return array
    },
    async getHotEntities() {
      const data = await d3.csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vR2hLJlo2hO6s1mvmTkRFHRhrBNOGTMgmkT_NHDEBI8-raXSar7z3HKm5r1pd5XeM-3Ll_qQhXhUNfl/pub?gid=2116993857&single=true&output=csv')
      this.entities = [
        ...this.shuffle(data.filter(row => row.grupo === '1')).slice(0, 2),
        ...this.shuffle(data.filter(row => row.grupo === '2')).slice(0, 2),
      ].map(row => row.nombre)
    },
    async getHotCases() {
      const data = await d3.csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vR2hLJlo2hO6s1mvmTkRFHRhrBNOGTMgmkT_NHDEBI8-raXSar7z3HKm5r1pd5XeM-3Ll_qQhXhUNfl/pub?gid=2096219490&single=true&output=csv')
      this.cases = [
        ...this.shuffle(data.filter(row => row.grupo === '1')).slice(0, 2),
        ...this.shuffle(data.filter(row => row.grupo === '2')).slice(0, 2),
      ].map(row => row.expediente.replace('/', '-'))
    },
    async getHotMagistrates() {
      const data = await d3.csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vR2hLJlo2hO6s1mvmTkRFHRhrBNOGTMgmkT_NHDEBI8-raXSar7z3HKm5r1pd5XeM-3Ll_qQhXhUNfl/pub?gid=0&single=true&output=csv')
      this.magistrates = [
        ...this.shuffle(data.filter(row => row.grupo === '1')).slice(0, 2),
        ...this.shuffle(data.filter(row => row.grupo === '2')).slice(0, 2),
      ].map(row => row.nombre)
    },
  }
}
</script>

<style scoped>
.container {
  padding-top: 60px;
}

.container:nth-child(3) {
  padding-bottom: 60px;
}
</style>
