<template>
  <section id="main" class="has-text-centered">
    <!-- Entidades -->
    <div v-if="entities.length > 0" class="container">
      <h2 class="title is-2">Personas destacadas</h2>

      <div class="columns">
        <card-entity v-if="entities[0] !== undefined" :name="entities[0]"></card-entity>
        <card-entity v-if="entities[1] !== undefined" :name="entities[1]"></card-entity>
        <card-entity v-if="entities[2] !== undefined" :name="entities[2]"></card-entity>
        <card-entity v-if="entities[3] !== undefined" :name="entities[3]"></card-entity>
      </div>
    </div><!--/container -->

    <!-- Causas -->
    <div v-if="cases.length > 0" class="container">
      <h2 class="title is-2">Causas relevantes</h2>

      <div class="columns">
        <card-case v-if="cases[0] !== undefined" :name="cases[0]"></card-case>
        <card-case v-if="cases[1] !== undefined" :name="cases[1]"></card-case>
        <card-case v-if="cases[2] !== undefined" :name="cases[2]"></card-case>
        <card-case v-if="cases[3] !== undefined" :name="cases[3]"></card-case>
      </div>
    </div><!--/container -->

    <!-- Magistrados -->
    <div v-if="magistrates.length > 0" class="container">
    <!-- <div v-if="false" class="container"> -->
      <h2 class="title is-2">Juezas/ces y Fiscales</h2>

      <div class="columns">
        <card-magistrate v-if="magistrates[0] !== undefined" :name="magistrates[0]"></card-magistrate>
        <card-magistrate v-if="magistrates[1] !== undefined" :name="magistrates[1]"></card-magistrate>
        <card-magistrate v-if="magistrates[2] !== undefined" :name="magistrates[2]"></card-magistrate>
        <card-magistrate v-if="magistrates[3] !== undefined" :name="magistrates[3]"></card-magistrate>
      </div>
    </div><!--/container -->
  </section>
</template>

<script>
import * as d3 from 'd3'
import axios from 'axios'
import CardEntity from '~/components/HomeHotCardEntity'
import CardCase from '~/components/HomeHotCardCase'
import CardMagistrate from '~/components/HomeHotCardMagistrate'

export default {
  data () {
    return {
      entities: [],
      cases: [],
      magistrates: []
    }
  },
  components: {
    CardEntity,
    CardCase,
    CardMagistrate
  },
  mounted () {
    this.getHotEntities()
    this.getHotCases()
    this.getHotMagistrates()
  },
  methods: {
    getHotEntities: function () {
      /*
      Descargo el csv con las entidades "hot" para poner en el home.
      Las entidades del grupo 0 van a estar siempre. Los demas grupos los sorteo.
      */
      let url = 'https://docs.google.com/spreadsheets/d/17pOcSqgidnPtQudN8y6Cog3QA6c_WoEEGFHv4oyV_bM/edit#gid=0'
      axios.get(url, { crossdomain: true }).then(result => {          
          let text = result.data
          let data = text.split("DIVIDER")[1]          
          let array = data.split("\n")
          let dictionary = []
          array.forEach(d => {
              let e = d.split(",")
              let grupo = e[0]
              let entidad = e[1]                            
              if (entidad !== undefined && grupo !== undefined) {               
                return dictionary.push({"grupo":grupo,"entidad":entidad})
              }
          })
          let groups = []                
          dictionary.forEach(d => {
              return groups.push(d.grupo) 
          })            
          console.log("dictionary",dictionary);    
          let groupRan = groups[Math.floor(Math.random() * groups.length)]                
          let filter_groups = ["0", groupRan]         
          let numeroAleatorio = Math.floor(Math.random() * (3) ) + 1;
          let resultado = []
          resultado[0]=dictionary[0].entidad
          resultado[1]=dictionary[1].entidad
          resultado[2]=dictionary[numeroAleatorio+numeroAleatorio].entidad
          resultado[3]=dictionary[numeroAleatorio+numeroAleatorio+1].entidad
          this.entities = resultado                      
      });
    },
    getHotCases: function () {
      /*
      Descargo el csv con las causas "hot" para poner en el home
      */

      let url = 'https://docs.google.com/spreadsheets/d/1qP1B8ECwJX-DJb92fduiIUk3my7ks2TklgXnGsZ96Lo/edit#gid=0'
      axios.get(url, { crossdomain: true }).then(result => {          
          let text = result.data
          let data = text.split("DIVIDER")[1]          
          let array = data.split("\n")          
          let dictionary = []
          array.forEach(d => {
              let e = d.split(",")
              let grupo = e[0]
              let expediente = e[1]
              let nombre = e[2]
              if (grupo !== undefined && 
                  nombre !== undefined &&
                  expediente !== undefined) return dictionary.push({"grupo":grupo,"expediente":expediente,"nombre":nombre})
          })
          let groups = []                
          dictionary.forEach(d => {
              return groups.push(d.grupo) 
          })                
          
          let groupRandom = dictionary[Math.floor(Math.random() * dictionary.length)]['grupo']               
          this.cases = dictionary.filter(d => d.grupo === groupRandom).map(d => d.expediente.replace('/', '-'))       
                   
      });
    },
    getHotMagistrates: function () {
      let url = 'https://docs.google.com/spreadsheets/d/1tRkXHJfbTmlwwT--a1Gf-f86gcdKNN0gN0o--Xre4oc/edit#gid=0'
      axios.get(url, { crossdomain: true }).then(result => {        
        let text = result.data
        let data = text.split("DIVIDER")[1]        
        let array = data.split("\n")              
        let dictionary = []
        array.forEach(d => {
            let e = d.split(",")
            let grupo = e[0]
            let entidad = e[1]
            if (grupo !== undefined && 
                entidad !== undefined) return dictionary.push({"grupo":grupo,"entidad":entidad})
        })
        let groupRandom = dictionary[Math.floor(Math.random() * dictionary.length)]['grupo']
        this.magistrates = dictionary.filter(d => d.grupo === groupRandom).map(d => d.entidad)        
      });
    }
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
