<template>
  <section id="estadisticas">
    <div v-if="Object.keys(entity).length !== 0" class="container">
      <base-buttons-share section="estadisticas" title="Relación con las causas"></base-buttons-share>

      <p class="d">
        Sobre la totalidad de causas, abiertas o cerradas, en la que figura {{ this.entity.nombre }}
      </p>

      <b-tabs>
        <b-tab-item label="Causas segun juez/a de instrucción de la causa">
          <bar id="segunJuez" :data="countJudge" :maxVal="maxVal"></bar>
        </b-tab-item>

        <b-tab-item label="Causas segun fiscal">
          <bar id="segunFiscal" :data="countFiscal" :maxVal="maxVal"></bar>
        </b-tab-item>

        <b-tab-item label="Relación con las causas">
          <bubble id="relacionCausas" :data="countRelations" />
        </b-tab-item>

        <b-tab-item label="Causas segun delito">
          <bubble id="delitos" :data="countCrimes" />

          <p>
            Nota: El gráfico anterior muestra la cantidad de causas en las que se le imputa
            cada uno de estos delitos. En cada causas se le puede imputar más de un delito.
          </p>
        </b-tab-item>
      </b-tabs>

    </div>
  </section>
</template>

<script>
import * as d3 from 'd3'
import Bar from '@/components/Charts/Bar'
import Bubble from '@/components/Charts/Bubble'
import BaseButtonsShare from '@/components/BaseButtonsShare'

export default {
  data () {
    return {
      maxVal: -1,
      countJudge: [],
      countFiscal: [],
      countRelations: [],
      countCrimes: [],

      caseState: [],
    }
  },
  props: {
    entity: {
      type: Object,
      required: true
    }
  },
  components: {
    Bar,
    Bubble,
    BaseButtonsShare,
  },
  watch: {
    entity: function () {
      this.maxVal = -1
      this.countJudge = []
      this.countFiscal = []
      this.countRelations = []
      this.countCrimes = []
      this.caseState = []

      this.calc()
    }
  },
  methods: {
    calc: function () {
      this.title = this.entity.tipo === 'organismo estatal' ? 'Descripcion' : 'Biografia'

      // Cases States
      let temp = []
      let temp2 = []
      this.entity.causas.forEach(cases => temp.push(cases.estado))
      this.caseState = temp.reduce((prev, curr) => (prev[curr] = ++prev[curr] || 1, prev), {})

      // Jugde count
      temp = []
      temp2 = []
      this.entity.causas.forEach(cases => temp.push(cases.juez.nombre))
      temp2 = temp.reduce((prev, curr) => (prev[curr] = ++prev[curr] || 1, prev), {})
      Object.keys(temp2).forEach(key => this.countJudge.push({ name: key, value: temp2[key] }))

      // Fiscal count
      temp = []
      temp2 = []
      this.entity.causas.forEach(cases => temp.push(cases.fiscal.nombre))
      temp2 = temp.reduce((prev, curr) => (prev[curr] = ++prev[curr] || 1, prev), {})
      Object.keys(temp2).forEach(key => this.countFiscal.push({ name: key, value: temp2[key] }))

      // Relation count
      temp = []
      temp2 = []
      this.entity.causas.forEach(cases => temp.push(cases.relacion))
      temp2 = temp.reduce((prev, curr) => (prev[curr] = ++prev[curr] || 1, prev), {})
      Object.keys(temp2).forEach(key => this.countRelations.push({ name: key, value: temp2[key] }))

      // Crimenes count
      temp = []
      temp2 = []
      let validInvolved = ['denunciante', 'querellante', 'sobreseido', 'investigado/a']
      this.entity.causas.forEach(cases => {
          temp = temp.concat(cases.delitos)
      })
      temp2 = temp.reduce((prev, curr) => (prev[curr] = ++prev[curr] || 1, prev), {})
      Object.keys(temp2).forEach(key => this.countCrimes.push({ name: key, value: temp2[key] }))

      // Sort
      this.countJudge = this.countJudge.sort((a, b) => a.value - b.value)
      this.countFiscal = this.countFiscal.sort((a, b) => a.value - b.value)
      this.countCrimes = this.countCrimes.sort((a, b) => b.value - a.value)

      this.maxVal = d3.max([this.countJudge[this.countJudge.length - 1].value,
                            this.countFiscal[this.countFiscal.length - 1].value])
    }
  }
}
</script>
