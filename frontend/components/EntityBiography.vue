<template>
  <section id="biografia">
    <div v-if="Object.keys(entity).length !== 0" class="container">
      <base-buttons-share section="biografia" :title="title" :data="entity.causas" plotName="casesEvolution"></base-buttons-share>

      <div v-if="entity.tipo !== 'organismo estatal'" class="columns is-tablet">
        <div v-if="entity.foto !== ''" class="column is-4">
          <figure class="image is-1by1">
            <img :src="baseUrl + 'fotos_entidades/' + entity.foto" class="border" />
          </figure>
        </div>

        <div v-if="entity.bio !== ''" class="column is-offset-1 is-7 s">
          <p>{{ this.entity.bio }}</p>
        </div><!--/column -->
      </div><!--/columns -->

      <div v-else class="columns">
        <div class="s">
          <p>{{ this.entity.bio }}</p>
        </div><!--/column -->
      </div>

      <!-- Total de causas -->
      <div class="level">
        <div v-for="relation in countRelations" :key="relation.id" class="level-item has-text-centered">
          <div class="box">
            <p class="heading">{{ relation.name }}</p>
            <p class="title">{{ relation.value }}</p>
          </div>
        </div>
      </div>

      <CasesEvolution v-if="entity.causas.length !== 0"
        :cases="entity.causas" :name="entity.nombre"></CasesEvolution>

    </div><!--/container -->
  </section><!--/biography -->
</template>

<script>
import { baseUrl } from '~/assets/utils'
import BaseButtonsShare from '~/components/BaseButtonsShare'
import CasesEvolution from '~/components/EntityBiographyCasesEvolution'

export default {
  data () {
    return {
      baseUrl: baseUrl,
      title: '',

      countRelations: []
    }
  },
  props: {
    entity: {
      type: Object,
      required: true
    }
  },
  components: {
    BaseButtonsShare,
    CasesEvolution
  },
  watch: {
    entity: function () {
      this.calc()
    }
  },
  methods: {
    calc: function () {
      this.title = this.entity.tipo === 'organismo estatal' ? 'Descripción' : 'Biografía'
      this.countRelations = []

      // Relation count
      let temp = []
      let temp2 = []
      this.entity.causas.forEach(cases => temp.push(cases.relacion))
      temp2 = temp.reduce((prev, curr) => (prev[curr] = ++prev[curr] || 1, prev), {})
      Object.keys(temp2).forEach(key => this.countRelations.push({ name: key, value: temp2[key] }))
    }
  }
}
</script>

<style scoped>
.s {
  padding-top: 25px;
}

.s p {
  font-size: 1.1rem;
}

.level {
  padding-top: 50px;
  padding-bottom: 50px;
}

.box {
  box-shadow: 5px 5px 2px 1px rgba(0, 0, 255, .2);
}

body.night .box {
  background-color: #0a121b;
  box-shadow: 5px 5px 2px 1px rgba(255, 255, 255, .2);
}
</style>
