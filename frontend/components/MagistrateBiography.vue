<template>
  <section id="biografia">
    <div v-if="Object.keys(magistrate).length !== 0" class="container">
      <base-buttons-share section="biografia" title="Biografia"></base-buttons-share>

      <div class="columns is-tablet">
        <div class="column is-4">
          <figure class="image is-1by1">
            <img :src="`${baseUrl}fotos_magistrados/${magistrate.nombre}.jpg`" class="border" />
          </figure>

          <div class="justi" v-if="magistrate.link_justiciopedia">
            <a class="title is-5" :href="magistrate.link_justiciopedia" target="_blank">
              Ver en <img src="~/assets/img/logo-justiciapedia.svg" />
            </a>
          </div>
        </div>

        <div class="column is-offset-1 is-7 s">
          <p>{{ this.showFullBio ? this.magistrate.bio : ( this.magistrate.bio !== undefined && this.magistrate.bio.slice(0, 1000)) }}</p>
          <button class="button" @click="showFullBio = !showFullBio">
            {{ this.showFullBio ? 'Ver menos' : 'Ver más' }}
          </button>
        </div><!--/column -->
      </div><!--/columns -->

    </div>
  </section>
</template>

<script>
import { baseUrl } from '~/assets/utils'
import BaseButtonsShare from '~/components/BaseButtonsShare'

export default {
  data () {
    return {
      baseUrl: baseUrl,
      showFullBio: false
    }
  },  
  props: {
    magistrate: {
      type: Object,
      required: true
    }
  },
  components: {
    BaseButtonsShare
  }
}
</script>

<style scoped>
.justi {
  padding-top: 15px;
  text-align: center;
}

.justi a {
  display: inline-flex;
}

.justi a:hover {
  color: #3273dc;
}

.justi img {
  width: 150px;
  padding-left: 10px;
}
</style>
