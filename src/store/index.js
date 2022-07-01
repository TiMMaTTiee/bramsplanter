import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import auth from './modules/auth'
import status from './modules/status'
import data from './modules/data'
import createPersistedState from 'vuex-persistedstate'

import { createStore, createLogger  } from 'vuex'

// Make Axios play nice with Django CSRF
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

const store = createStore({
  modules: {
    auth,
    status,
    data
  },

  plugins: [createPersistedState()],

  state: {
  },

  mutations: {
  }
})

export default store;