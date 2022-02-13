import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import auth from './modules/auth'
import status from './modules/status'
import data from './modules/data'
import plots from './modules/plots'
import createPersistedState from 'vuex-persistedstate'

Vue.use(Vuex)

// Make Axios play nice with Django CSRF
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

export default new Vuex.Store({
  modules: {
    auth,
    status,
    data,
    plots
  },

  plugins: [createPersistedState()],

  state: {
  },

  mutations: {
  }
})
