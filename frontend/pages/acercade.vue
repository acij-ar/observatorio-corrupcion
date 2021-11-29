<template>
  <div>
    <portal to="header">
      <div class="hero-body">
        <h1 class="title">
          Acerca de
        </h1>
      </div>
    </portal>
    <acerca-de></acerca-de>
  </div>
</template>



<script>
import AcercaDe from '@/components/AcercaDe'
export default {
  head () {
    return {
      title: 'Estadisticas Generales'
    }
  },
  components: {
    AcercaDe
  }
}
</script>
