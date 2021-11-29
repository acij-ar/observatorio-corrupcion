<template>
  <div>

    <div class="loading-page" v-if="loading">
      <p>Cargando...</p>
    </div>

    <the-nav-bar v-on:changeCSSMode="(e) => this.mode=e" v-if="!loading"></the-nav-bar>

    <nuxt v-if="!loading"/>

    <the-contact v-if="!loading"></the-contact>
    <the-footer v-if="!loading"></the-footer>

    <!-- Tooltip for the plots -->
    <div id="tooltip" class="hidden"><p id="value"></p></div>
  </div>
</template>

<script>
import TheNavBar from '@/components/TheNavBar'
import TheContact from '@/components/TheContact'
import TheFooter from '@/components/TheFooter'

export default {
  data () {
    return {
      mode: 'day',
      loading: false, 
    }
  },
  head () {
    return {
      bodyAttrs: {
        class: this.mode
      }
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.loading = true     
      setTimeout(() => this.loading = false, 3000)
    })
  }, 
  components: {
    TheNavBar,
    TheContact,
    TheFooter
  }
}
</script>

<style scoped>
.loading-page {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.8);
  text-align: center;
  padding-top: 200px;
  font-size: 30px;
  font-family: sans-serif;
}
</style>
