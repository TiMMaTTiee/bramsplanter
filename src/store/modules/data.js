import apiService from '../../services/apiService'

/* eslint-disable */
const state = {
  temp: null,
  moist: null,
  cells: null,
  recent: null,
  recentImage: null,
  timeType: 'hour',
  timeCount: 5
}

const getters = {
  temp: state => {
    return state.temp
  },
  moist: state => {
    return state.moist
  },
  cells: state => {
    return state.cells
  },
  recent: state => {
    return state.recent
  },
  recentImage: state => {
    return state.recentImage
  },
  timeType: state => {
    return state.timeType
  },
  timeCount: state => {
    return state.timeCount
  }
}

const actions = {
  async getTemp({ commit }, { args }) {
    var path = 'temp_data'
    var result = await apiService.apiRequest(path, args)
    commit('setTemp', result.data)
  },
  async getMoist({ commit }, { args }) {
    var path = 'all_data'
    var result = await apiService.apiRequest(path, args)
    commit('setMoist', result.data)
  },
  async getCells({ commit }, { args }) {
    var path = 'cell_data'
    var result = await apiService.apiRequest(path, args)
    commit('setCells', result.data)
  },
  async getRecent({ commit }, { args }) {
    var path = 'recent_data'
    var result = await apiService.apiRequest(path, args)
    commit('setRecent', result.data)
  },
  async getRecentImage({ commit }, { args }) {
    var path = 'recent_image'
    var result = await apiService.apiRequest(path, args)
    commit('setRecentImage', result.data)
  },
  setTimeType({ commit }, timeType) {
    commit('newTimeType', timeType)
  },
  setTimeCount({ commit }, timeCount) {
    commit('newTimeCount', timeCount)
  }
}

const mutations = {
  setTemp(state, value) {
    state.temp = value
  },
  setMoist(state, value) {
    state.moist = value
  },
  setCells(state, value) {
    state.cells = value
  },
  setRecent(state, value) {
    state.recent = value
  },
  setRecentImage(state, value) {
    state.recentImage = value
  },
  newTimeType(state, value) {
    state.timeType = value
  },
  newTimeCount(state, value) {
    state.timeCount = value
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
