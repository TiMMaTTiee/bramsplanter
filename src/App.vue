<template>
  <div id="app">
    <!-- NavBar -->
    <b-navbar id="navbar" sticky type="dark" variant="dark">
      <b-img height="50rem" :src="getImgUrl(logoImage)"></b-img>
      <b-navbar-nav>
        <b-nav-item :to="{ name: 'home' }">Home</b-nav-item>
      </b-navbar-nav>
      <b-navbar-nav class="ml-auto navbar-right">
        <b-nav-item>
          <Login v-if="!$store.state.auth.user.isAuthenticated">Login</Login>
          <b-link
            v-if="$store.state.auth.user.isAuthenticated"
            v-on:click="onClickLogout"
            >Logout {{ $store.state.auth.user.name }}</b-link
          >
        </b-nav-item>
      </b-navbar-nav>
    </b-navbar>
    <router-view v-if="isAuthenticated" id="router-view" class="page" />
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

import Home from './components/Home.vue'
import Login from '@/components/Login'

/* eslint-disable */

export default {
  name: 'app',
  components: {
    Home,
    Login,
  },
  data() {
    return {
      logoImage: 'logo.png',
    }
  },
  methods: {
    returnHome() {
      this.$router.push({ name: 'home' })
    },
    ...mapActions('auth', ['authenticate', 'logout']),
    ...mapActions('plots', ['setActivePlot']),
    onClickLogout() {
      this.setActivePlot({ name: '', id: -1, api_key: '' })

      this.logout()
      this.returnHome()
    },
    getImgUrl(pic) {
      return require('./assets/' + pic)
    },
  },
  created() {
    this.authenticate()
  },
  watch: {},
  computed: mapState({
    isAuthenticated: (state) => state.auth.user.isAuthenticated,
  }),
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: rgb(241, 241, 241);
}

body {
  background-color: rgb(209, 209, 209);
}

.container,
.container-sm,
.container-md,
.container-lg {
  max-width: 100%;
  min-width: 80%;
}

/* Header & navbar */
#navbar {
  margin-bottom: 2rem;
  background-color: #00335f !important;
}
.nav-item.nav-item.nav-item a {
  color: whitesmoke;
}
.nav-item.nav-item.nav-item ul {
  background-color: #3d4348;
}
.nav-item.nav-item.nav-item a {
  color: whitesmoke;
}
.nav-item.nav-item.nav-item ul {
  background-color: #3d4348;
}
.header {
  background-color: #ffffff;
  padding-left: 20rem;
}
.panel {
  background-color: white;
  padding: 2rem;
  margin: 1rem;
}
.scroll-container {
  max-height: 50vh;
  height: auto;
  overflow-y: scroll;
  margin-top: 1rem;
}

h3 {
  clear: both;
  float: left;
  width: 100%;
}
</style>
