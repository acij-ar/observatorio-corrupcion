<template>
  <section id="investigados">
    <div v-if="Object.keys(magistrate).length !== 0" class="container">
      <base-buttons-share section="invenstigados" title="10 más investigados/as"
        plotName="masIvenstigados"></base-buttons-share>

      <bar id="masIvenstigados" :data="magistrate.mas_investigados"></bar>
    </div>
  </section>
</template>

<script>
import { baseUrl } from '~/assets/utils'
import Bar from '@/components/Charts/Bar'
import BaseButtonsShare from '~/components/BaseButtonsShare'

export default {
  data () {
    return {
      baseUrl: baseUrl
    }
  },
  props: {
    magistrate: {
      type: Object,
      required: true
    }
  },
  components: {
    Bar,
    BaseButtonsShare
  }
}
</script>
