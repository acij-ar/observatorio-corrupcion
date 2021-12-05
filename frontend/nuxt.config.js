const pkg = require('./package')

module.exports = {
  ssr: false,

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
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      { rel: "preconnect", href: "https://fonts.googleapis.com" },
      { rel: "preconnect", href:"https://fonts.gstatic.com", crossorigin: true },
      { href: "https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600&display=swap", rel: "stylesheet" }
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
    '~/assets/scss/main.scss'
  ],

  styleResources: {
    scss: ['./assets/scss/*.scss']
  },

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
    'nuxt-buefy',
    '@nuxtjs/style-resources',
  ],

  buildModules: [
    '@nuxtjs/google-analytics'
  ],
  googleAnalytics: {
    id: 'UA-213809731-1'
  },

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
