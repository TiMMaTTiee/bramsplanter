import apiService from '../../services/apiService'

/* eslint-disable */
const state = {
    activeSettings: null,
    moduleStatuses: null,
    hardwareStatuses: null,
    activeProgram: null
}

const getters = {
    settings: state => {
        return state.activeSettings
    },
    moduleStatuses: state => {
      return state.moduleStatuses
    },
    hardwareStatuses: state => {
      return state.hardwareStatuses
    },
    activeProgram: state => {
      return state.activeProgram
    }
}

const actions = {
  async getSettings({commit}) {
    var path = 'active_settings'
    var args = []
    var result = await apiService.apiRequest(path, args)
    commit('setSettings', result.data)
  },
  async getModuleStatuses({commit}) {
    var path = 'module_statuses'
    var args = []
    var result = await apiService.apiRequest(path, args)
    commit('setModuleStatuses', result.data.data)
  },
  async getHardwareStatuses({commit}) {
    var path = 'hardware_statuses'
    var args = []
    var result = await apiService.apiRequest(path, args)
    commit('setHardwareStatuses', result.data)
  },
  async getActiveProgram({commit}) {
    var path = 'active_program'
    var args = []
    var result = await apiService.apiRequest(path, args)
    commit('setProgram', result.data)
  }
}

const mutations = {
  setSettings(state, value) {
    state.activeSettings = value
  },
  setModuleStatuses(state, value) {
    state.moduleStatuses = value
  },
  setHardwareStatuses(state, value) {
    state.hardwareStatuses = value
  },
  setProgram(state, value) {
    state.activeProgram = value
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
