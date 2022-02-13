<template>
  <b-container>
    <b-row class="panel">
      <b-col style="margin: 0rem 1rem 0rem 0rem">
        <h1>Hi {{ $store.state.auth.user.name }}</h1>
      </b-col>
      <b-col>
        <b-dropdown id="dropdown-1" :text="$store.state.plots.activePlot.name" class="m-md-2">
          <b-dropdown-item v-for="plot in plots" :key="plot.id" @click="selectPlot(plot)">
            {{ plot.name }}
          </b-dropdown-item>
        </b-dropdown>
      </b-col>
    </b-row>
    <b-row class="panel">
      <RecentDataView />
    </b-row>
    <b-row class="panel">
      <PlotView />
    </b-row>
    <b-row class="panel">
      <EspSettingsView />
    </b-row>
    <b-row> </b-row>
  </b-container>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import moment from 'moment'
import PlotView from './Plot.vue'
import RecentDataView from './RecentData.vue'
import EspSettingsView from './EspSettings.vue'

export default {
  name: 'Home',
  data () {
    return {
      userName: 'null',
      activePlot: { name: 'plot1', id: 1 },
      plots: this.$store.state.plots.plots.data
    }
  },
  components: {
    PlotView,
    RecentDataView,
    EspSettingsView
  },
  computed: {
    ...mapState({
      currentUser: (state) => state.auth.user,
      currentPlot: (state) => state.plots.activePlot,
      currentPlots: (state) => state.plots.plots
    }),
    timeAgo (time) {
      return moment(time).fromNow()
    }
  },
  methods: {
    ...mapActions('auth', ['user']),
    ...mapActions('plots', ['getPlots', 'setActivePlot']),
    ...mapActions('data', ['setTimeCount', 'setTimeType']),
    ...mapActions('status', ['getEspSettings']),
    selectPlot (plot) {
      this.setActivePlot(plot)
    }
  },
  created () {
    this.getPlots({
      args: [
        this.$store.state.auth.user.uuid
      ]
    })
  },
  watch: {
    currentUser: {
      deep: true,
      handler (user) {
        this.userName = user.name
        this.getPlots({
          args: [
            this.$store.state.auth.user.uuid
          ]
        })
      }
    },
    currentPlot (plot) {
      this.activePlot = plot
      this.getEspSettings({ args: [this.$store.state.plots.activePlot.api_key] })
      this.setTimeCount(5)
      this.setTimeType('hour')
    },
    currentPlots (plots) {
      this.plots = plots.data
      this.selectPlot(plots[0])
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
