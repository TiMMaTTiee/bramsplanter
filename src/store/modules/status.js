import apiService from '../../services/apiService'

/* eslint-disable */
const state = {
  espSettings: null,
  sendStatus: null
}

const getters = {
  settings: state => {
    return state.activeSettings
  },
  sendStatus: state => {
    return state.sendStatus
  },
}

const actions = {
  async getEspSettings({ commit }, { args }) {
    var path = 'get_esp_settings_uuid'
    var result = await apiService.apiRequest(path, args)
    commit('setEspSettings', result.data)
  },
  async setEspSettings({ commit }, { args }) {
    var path = 'set_esp_settings'
    var result = await apiService.apiRequest(path, args)
    commit('setSendStatus', result.data)
  },
}

const mutations = {
  setEspSettings(state, value) {
    state.espSettings = value
  },
  setSendStatus(state, value) {
    state.sendStatus = value
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
