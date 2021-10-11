import authService from '../../services/authService'

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
  authenticate ({commit}, credentials) {
    if (credentials) {
      const {username, password} = credentials;
      return authService.verifyUser({username, password})
      .then(auth => {
        console.log('response' + auth.data)
        commit('setUser', {user:{name:username, password:password, isAuthenticated:true}})
      })
      .catch((error) => {
        // eslint-disable-next-line
        console.error(error)
      });
    } 
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
