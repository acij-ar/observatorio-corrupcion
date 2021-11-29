<template>
  <header>
    <nav class="navbar f">
      <div class="container">

        <div class="navbar-brand">
          <nuxt-link to="/" class="navbar-item">
            <img src="~@/assets/logo_observatorio.png" alt="logo observatorio de causas de Corrupcion" />
          </nuxt-link>
          <span class="navbar-burger burger" data-target="navbarMenuHeroA">
            <span></span>
            <span></span>
            <span></span>
          </span>
        </div>

        <div id="navbarMenuHeroA" class="navbar-menu">
          <div class="navbar-end">
            <nuxt-link to="/" class="navbar-item">
              Inicio
            </nuxt-link>
            <router-link to="/estadisticas" class="navbar-item">
              Estadísticas
            </router-link>
            <router-link to="/acercade" class="navbar-item">
              Acerca de
            </router-link>
            <a class="navbar-item">
              Glosario
            </a>
            <a class="navbar-item">
              Nosotros
            </a>
            <a class="navbar-item">
              API
            </a>
            <a class="social-item gitlab">
              <font-awesome-icon :icon="{ prefix: 'fab', iconName: 'gitlab' }"/>
            </a>

            <!-- Change to light or dark mode -->
            <div class="aa">
              <font-awesome-icon :icon="{ prefix: 'far', iconName: 'sun' }"/>
              <b-switch v-model="isSwitched" size="is-small"></b-switch>
              <font-awesome-icon :icon="{ prefix: 'far', iconName: 'moon' }"/>
            </div>
          </div>
        </div>
      </div><!--/container -->
    </nav>
    <div class="hero">
      <div class="container has-text-centered">
        <portal-target name="header" />
      </div>
    </div>
  </header>
</template>

<script>
export default {
  head () {
    return {
      bodyAttrs: {
        class: this.theme
      }
    }
  },
  data () {
    return {
      theme: null,
      isSwitched: false
    }
  },
  watch: {
    isSwitched: function () {
      this.theme = this.isSwitched === true ? 'night' : 'day'
      localStorage.setItem('theme', this.theme)
    }
  },
  mounted () {
    const localTheme = localStorage.getItem('theme')
    this.theme = ['night', 'day'].includes(localTheme) ? localTheme : 'day'
    this.isSwitched = this.theme === 'night'
  },
}
</script>

<style scoped>
.f {
  position: absolute;
  left: 0;
  right: 0;
  background: transparent;
}

.navbar-item img {
  max-height: 3.5rem;
}

/*
  Links
*/
.navbar-item {
  padding-top: 25px;
}

.navbar-brand a.navbar-item {
  padding-top: 10px;
}

.navbar-brand a.navbar-item.nuxt-link-exact-active::after,
.navbar-brand a.navbar-item::after {
  height: 0px;
}

a.navbar-item, a.navbar-item.nuxt-link-exact-active {
  color: whitesmoke;
  font-size: 1.1rem;
  font-weight: bold;
  font-family: BisionBold;
  display: inline-block;
}

a.navbar-item.nuxt-link-exact-active::after {
  content: '';
  display: block;
  width: 100%;
  height: 4px;
  background: #d63533;
}

a.navbar-item:hover {
  background: transparent;
  color: whitesmoke;
  border-width: 4px;
}

a.navbar-item::after {
  content: '';
  display: block;
  width: 0;
  height: 4px;
  background: #d63533;
  transition: width .3s;
}

a.navbar-item:hover::after {
  width: 100%;
}

.social-item {
  line-height: 1.5;
  padding: 0.5rem 1rem;
  padding-top: 25px;
  color: white;
  position: relative;
}

.twitter:hover {
  color: #1da1f2;
}

.gitlab:hover {
  color: #fc6d26;
}

.navbar-menu div.aa {
  padding-top: 25px;
  padding-left: 1rem;
}

.navbar-menu div.aa svg {
  color: white;
}
</style>
