import apiService from '../../services/apiService'

/* eslint-disable */
const state = {
  espSettings: null
}

const getters = {
  settings: state => {
    return state.activeSettings
  }
}

const actions = {
  async getEspSettings({ commit }, { args }) {
    var path = 'get-esp-settings-uuid'
    var result = await apiService.apiRequest(path, args)
    commit('setEspSettings', result.data)
  }
}

const mutations = {
  setEspSettings(state, value) {
    state.espSettings = value
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
