<template>
  <b-container>
    <h1>Hi {{ $store.state.auth.user.name }}</h1>
  </b-container>
</template>

<script>

import { mapState, mapActions } from 'vuex'
import moment from 'moment'
export default {
  name: 'Home',
  data () {
    return {
      userName: 'null'
    }
  },
  components: {
  },
  computed: {
    ...mapState({
      currentUser: state => state.auth.user
    }),
    timeAgo (time) {
      return (moment(time).fromNow())
    }
  },
  methods: {
    ...mapActions('auth', ['user'])
  },
  watch: {
    currentUser (user) {
      console.log('New user: ', user.name)
      this.userName = user.name
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
