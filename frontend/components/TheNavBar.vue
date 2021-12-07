<template>
  <header>
    <b-navbar class="container is-fluid">
      <template #brand>
        <b-navbar-item tag="router-link" to="/">
          <nuxt-link to="/" class="navbar-item">
            <img src="~@/assets/img/logo_observatorio.png" alt="logo observatorio de causas de Corrupcion" />
          </nuxt-link>
        </b-navbar-item>
      </template>
      <template #end>
        <nuxt-link to="/" class="navbar-item">
          Inicio
        </nuxt-link>
        <router-link to="/estadisticas" class="navbar-item">
          Estadísticas
        </router-link>
        <router-link to="/acerca-de" class="navbar-item">
          Acerca de
        </router-link>
        <router-link to="/glosario" class="navbar-item">
          Glosario
        </router-link>
        <router-link to="/nosotros" class="navbar-item">
          Nosotros
        </router-link>
        <a class="navbar-item" href="https://github.com/acij-ar/observatorio-corrupcion/raw/master/cij.zip">
          Datos
        </a>
        <a class="navbar-item" :href="`${backendUrl}swagger-ui/`" target="_blank">
          API
        </a>
        <a class="social-item gitlab" href="https://github.com/acij-ar/observatorio-corrupcion" target="_blank">
          <font-awesome-icon :icon="{ prefix: 'fab', iconName: 'github' }"/>
        </a>
        <div class="aa">
          <font-awesome-icon :icon="{ prefix: 'far', iconName: 'sun' }"/>
          <b-switch v-model="isSwitched" size="is-small"></b-switch>
          <font-awesome-icon :icon="{ prefix: 'far', iconName: 'moon' }"/>
        </div>
      </template>
    </b-navbar>

    <div class="hero">
      <div class="container has-text-centered">
        <portal-target name="header" />
      </div>
    </div>
  </header>
</template>

<script>
import { apiUrl } from '@/assets/utils'

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
      isSwitched: false,
      backendUrl: apiUrl.replace('/v1', ''),
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

<style lang="scss">
.navbar {
  position: absolute;
  left: 0;
  right: 0;
  background: transparent;
}

.navbar-burger {
  &:hover {
    color: white;
  }
  span {
    height: 2px;
    color: white;
    &:hover {
      color: white;
    }
  }
}

// .navbar-item 

/*
  Links
*/
.navbar-item {
  padding-top: 25px;

  img {
    max-height: 3.5rem;
  }
}

.navbar-brand {
  a.navbar-item {
    padding-top: 10px;
  }
  a.navbar-item::after,
  a.navbar-item.nuxt-link-exact-active::after {
    height: 0px;
  }
}

a.navbar-item,
a.navbar-item.nuxt-link-exact-active {
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
  background: $red;
}
a.navbar-item:focus,
a.navbar-item:focus-within {
  background: transparent;
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
  background: $red;
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

.gitlab:hover {
  color: $red;
}

.navbar-menu div.aa {
  padding-top: 25px;
  padding-left: 1rem;
}

.navbar-menu div.aa svg {
  color: white;
}

@media screen and (max-width: #{$width-table}) {
  .navbar-end {
    width: 100%;
    display: inline-grid;
    justify-items: center;
  }

  .day {
    .navbar-menu {
      background-color: $body-day;
      box-shadow: 0 8px 16px rgb(10 10 10 / 20%);
      .navbar-item,
      svg,
      div.aa svg {
        color: black;
      }
    }
  }
  .night {
    .navbar-menu {
      background-color: $body-dark;
      box-shadow: 0 8px 16px rgb(250 250 250 / 20%);
    }
  }
}
</style>
