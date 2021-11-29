<template>
  <div>
    <section id="banner" class="hero is-fullheight">
      <div class="hero-body">
        <div class="container">
          <h1 class="title">
            Observatorio de Causas de Corrupcion
          </h1>

          <b-field>
            <b-autocomplete
              type="search"
              icon="search-plus"
              v-model="entityPartialName"
              expanded
              :data="data"
              @keyup.native.enter="search"
              placeholder="personas, juezas/ces, fiscales, nombres de causas o número de expediente"
              field="nombre"
              :loading="isFetching"
              @input="getAsyncData"
              @select="option => entitySelected = option">

              <template slot-scope="props">
                <div>
                  <font-awesome-icon :icon="{ prefix: getPrefix(props.option), iconName: getIcon(props.option) }"/>
                  <p class="autocomplete-option">{{ props.option.nombre }}</p>
                </div>
              </template>
            </b-autocomplete>
          </b-field>

          <a class="ref-banner" href="/acercade?sector=1">
            ¿Qué tipo de información podés encontrar en este Observatorio?
          </a>

        </div>
      </div>
    </section>

    <home-hot></home-hot>
  </div>
</template>

<script>
import debounce from 'debounce'
import { HTTP } from '@/assets/utils'

import HomeHot from '~/components/HomeHot'

export default {
  head () {
    return {
      title: 'Inicio'
    }
  },
  data () {
    return {
      data: [],
      entityPartialName: null,
      entitySelected: null,
      isFetching: false,

      errors: []
    }
  },
  components: {
    HomeHot
  },
  watch: {
    entitySelected: function () {
      if (this.entitySelected && this.entitySelected.key !== '') {
        let name = this.entitySelected.tipo === 'expediente judicial' ? 'expediente'
          : this.entitySelected.tipo === 'magistrado' ? 'magistrado'
            : 'entidad'

        this.$router.push({
          name: name,
          query: { nombre: this.entitySelected.key }
        })
      }
    }
  },
  methods: {
    getPrefix: function (options) {
      let type = options.tipo
      let subtype = options.sub_tipo

      return type === 'expediente judicial' ? 'fas'
        : type === 'magistrado' ? 'fas'
          : type === 'organismo estatal' ? 'fas'
            : 'far'
    },
    getIcon: function (options) {
      let type = options.tipo
      let subtype = options.sub_tipo

      return type === 'expediente judicial' ? 'balance-scale'
        : subtype === 'juez' ? 'gavel'
          : subtype === 'fiscal' ? 'search'
            : type === 'organismo estatal' ? 'university'
              : 'user'
    },
    getAsyncData: debounce(function () {
      this.data = []
      this.isFetching = true

      if (this.entityPartialName !== '') {
        HTTP.get(`buscar?q=${this.entityPartialName}`)
          .then(response => {
            this.data = response.data.results
            this.isFetching = false

            if (response.data.results.length === 0) {
              this.data = [{ key: '', nombre: 'éste nombre no fue encontrado' }]
            }
          })
          .catch(error => {
            this.errors.push(error)
            this.isFetching = false
          })
      }
    }, 500)
  }
}
</script>

<style>
.autocomplete-option {
  display: inline-block;
  padding-left: 10px;
}

body.night .autocomplete-option {
  color: black;
}
</style>
