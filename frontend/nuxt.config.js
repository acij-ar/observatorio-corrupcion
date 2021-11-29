const pkg = require('./package')

module.exports = {
  mode: 'spa',

  server: {
    port: 3000, // default: 3000
    host: '0.0.0.0', // default: localhost
  },

  /*
  ** Headers of the page
  */
  head: {
    title: '',
    titleTemplate: '%s | Observatorio de la Corrupcion',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: pkg.description }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },

  /*
  ** Customize the progress-bar color
  */
  loading: { color: '#fff' },

  /*
  ** Global CSS
  */
  css: [
    '~/assets/css/main.css'
  ],

  /*
  ** Plugins to load before mounting the App
  */
  plugins: [
    '~/plugins/font-awesome',
    '~/plugins/portal',
  ],

  /*
  ** Nuxt.js modules
  */
  modules: [,
    // Doc: https://buefy.github.io/#/documentation
    'nuxt-buefy',
    ['nuxt-matomo', { matomoUrl: '//analytics.conocimientoabierto.org/', siteId: 4 }]
  ],

  /*
  ** Build configuration
  */
  build: {
    /*
    ** You can extend webpack config here
    */
    extend(config, ctx) {

    }
  }
}
