<template>
  <div>
    <section class="hero_secondary">
      <!-- Hero body -->
      <div class="hero-body">
        <div class="container has-text-centered">
          <h1 class="title">
            Acerca de
          </h1>
        </div>
      </div>
    </section>
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