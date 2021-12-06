<template>
  <div>
    <nuxt/>
    <the-contact></the-contact>
    <the-footer></the-footer>

    <!-- Tooltip for the plots -->
    <div id="tooltip" class="hidden"><p id="value"></p></div>
  </div>
</template>

<script>
import TheContact from '@/components/TheContact'
import TheFooter from '@/components/TheFooter'

export default {
  components: {
    TheContact,
    TheFooter
  }
}
</script>
