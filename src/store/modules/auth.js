import apiService from '../../services/apiService'

/* eslint-disable */
const state = {
  user: {name:null, password:null, isAuthenticated:false},
  isModalOpen: false,
}

const getters = {
  user: state => {
    return state.user
  },
  isModalOpen: state => {
    return state.isModalOpen
  }
}

const actions = {
  async authenticate ({commit}, {args}) {
    var path = 'verify_user'
    var result = await apiService.apiRequest(path, args)
    console.log('response' + result.data)
    console.log('request' + args)
    console.log('request ' + args[0])

    commit('setUser', {user:{name:args[0], password:'secret', isAuthenticated:true}})
  },
  logout ({commit}) {
    commit('setUser', {user:{name:null, password:null, isAuthenticated:false}})
    commit('toggleModal')
  },
  toggleModal ({commit}) {
    commit('toggleModal')
  }
}

const mutations = {
  setUser(state, {user}) {
    state.user = user
  },
  toggleModal(state) {
    state.isModalOpen = !state.isModalOpen;
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
