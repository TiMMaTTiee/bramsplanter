import apiService from '../../services/apiService'

/* eslint-disable */
const state = {
  plots: null,
  activePlot: { name: 'plot1', id: 1 }
}

const getters = {
  plots: state => {
    return state.plots
  },
  activePlot: state => {
    return state.activePlot
  }
}

const actions = {
  async getPlots({ commit }, { args }) {
    var path = 'plots_for_uuid'
    var result = await apiService.apiRequest(path, args)
    commit('setPlots', result.data)
  },
  setActivePlot({ commit }, plot) {
    commit('newActivePlot', plot)
  }
}

const mutations = {
  setPlots(state, value) {
    state.plots = value
  },
  newActivePlot(state, value) {
    state.activePlot = value
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
