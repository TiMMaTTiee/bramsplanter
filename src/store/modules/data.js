import apiService from '../../services/apiService'

/* eslint-disable */
const state = {
    counted: null,
    rejected: null,
    programs: null,
    timeType: 'hour',
    timeCount: 5
}

const getters = {
    counted: state => {
      return state.counted
    },
    rejected: state => {
      return state.rejected
    },
    programs: state => {
      return state.programs
    },
    timeType: state => {
      return state.timeType
    },
    timeCount: state => {
      return state.timeCount
    }
}

const actions = {
  async getCounted({commit}, {args}) {
    var path = 'counted_data'
    var result = await apiService.apiRequest(path, args)
    commit('setCounted', result.data)
  },
  async getRejected({commit}, {args}) {
    var path = 'rejected_data'
    var result = await apiService.apiRequest(path, args)
    commit('setRejected', result.data)
  },
  async getPrograms({commit}, {args}) {
    var path = 'programs_data'
    var result = await apiService.apiRequest(path, args)
    commit('setPrograms', result.data)
  },
  setTimeType({commit}, timeType) {
    commit('newTimeType', timeType)
  },
  setTimeCount({commit}, timeCount) {
    commit('newTimeCount', timeCount)
  }
}

const mutations = {
  setCounted(state, value) {
    state.counted = value
  },
  setRejected(state, value) {
    state.rejected = value
  },
  setPrograms(state, value) {
    state.programs = value
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
