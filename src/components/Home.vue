<template>
  <b-container>
    <b-row class="panel">
      <b-col style="margin: 0rem 1rem 0rem 0rem">
        <h1>Hi {{ $store.state.auth.user.name }}</h1>
      </b-col>
    </b-row>
    <b-row class="panel">
      <RecentDataView />
    </b-row>
    <b-row class="panel">
      <PlotView />
    </b-row>
    <b-row> </b-row>
  </b-container>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import moment from 'moment'
import PlotView from './Plot.vue'
import RecentDataView from './RecentData.vue'

export default {
  name: 'Home',
  data () {
    return {
      userName: 'null',
      plots: [
        { name: 'plot1', id: 1 },
        { name: 'plot2', id: 2 },
        { name: 'plot3', id: 3 }
      ]
    }
  },
  components: {
    PlotView,
    RecentDataView
  },
  computed: {
    ...mapState({
      currentUser: (state) => state.auth.user
    }),
    timeAgo (time) {
      return moment(time).fromNow()
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
