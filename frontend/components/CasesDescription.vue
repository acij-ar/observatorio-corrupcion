<template>
  <section id="descripcion">
    <div v-if="Object.keys(cases).length !== 0" class="container">
      <base-buttons-share section="resumen" title="Resumen"></base-buttons-share>

      <div class="columns is-tablet">
        <div class="column is-5">
          <figure class="image">
            <img :src="getLogoUrl(baseUrl,cases._key)"/>
          </figure>
          <p style="font-size: 0.9rem;">
            Fuente de la foto: {{ this.cases.fuente_foto }}
          </p>
        </div>

        <div class="column is-6 s">
          <p>
            <span class="title is-5">Caratula:</span> {{ this.cases.caratula }}
          </p>

          <p>
            <span class="title is-5">Fecha comienzo:</span> {{ this.cases.anio_comienzo }}
          </p>

          <p>
            <span class="title is-5">Estado actual:</span> {{ this.cases.estado }}
          </p>
        </div><!--/column -->
      </div><!--/columns -->

      <p>{{ this.cases.hechos }}</p>

    </div><!--/container -->
  </section>
</template>

<script>
import { baseUrl } from '~/assets/utils'
import BaseButtonsShare from '~/components/BaseButtonsShare'

export default {
  data () {
    return {
      baseUrl: baseUrl
    }
  },
  props: {
    cases: {
      type: Object,
      required: true
    }
  },
  components: {
    BaseButtonsShare
  },
  methods: {
    getLogoUrl: function (base,key) {          
      var path = window.location.origin;
      var image = new Image();
      var url_image = path+'/fotos_causas/'+key+'.jpg';
      image.src = url_image;
      let imagen = "";    
      if (image.width <= 1) {                
          imagen = base+"fotos_causas/unnamed.png";
      } else {          
          imagen = base+"fotos_causas/"+key+".jpg";
      }
      return imagen;      
    }
  }
}
</script>

<style scoped>
.s {
  padding-top: 20px;
}

.s p {
  padding-bottom: 20px;
}
</style>
