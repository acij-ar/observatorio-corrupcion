import Vue from 'vue'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faMoon, faSun, faUser } from '@fortawesome/free-regular-svg-icons'
import { faTwitter, faGitlab } from '@fortawesome/free-brands-svg-icons'
import { faUniversity, faSearch, faGavel, faBalanceScale } from '@fortawesome/free-solid-svg-icons'

// Unpack some font awesome icons
library.add(faTwitter, faGitlab, faMoon, faSun, faUniversity, faSearch, faGavel, faBalanceScale, faUser)
Vue.component('font-awesome-icon', FontAwesomeIcon)
