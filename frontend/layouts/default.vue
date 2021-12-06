<template>
  <div class="default">
    <the-nav-bar/>
    <nuxt/>
    <the-contact/>
    <the-footer/>

    <!-- Tooltip for the plots -->
    <div id="tooltip" class="hidden"><p id="value"></p></div>
  </div>
</template>

<script>
import TheNavBar from '@/components/TheNavBar'
import TheContact from '@/components/TheContact'
import TheFooter from '@/components/TheFooter'

export default {
  components: {
    TheNavBar,
    TheContact,
    TheFooter
  }
}
</script>
