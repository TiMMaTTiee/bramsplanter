<template>
  <b-row class="panel">
    <h3>Settings</h3>

    {{ currentSettings }}
  </b-row>
</template>

<script>
/* eslint-disable */
/* eslint-disable no-console */
import { mapState, mapActions } from 'vuex'
import moment from 'moment-timezone'

export default {
  name: 'EspSettingsView',
  data() {
    return {
      currentSettings: null,
    }
  },
  methods: {
    ...mapActions('status', ['getEspSettings']),
  },
  mounted() {},
  computed: {
    ...mapState({
      currentEspSettings: (state) => state.status.espSettings,
    }),
  },
  created() {
    this.getEspSettings({ args: [this.$store.state.auth.user.uuid] })
    this.intervalId = setInterval(() => {
      this.getEspSettings({ args: [this.$store.state.auth.user.uuid] })
    }, 10000)
  },
  beforeDestroy() {
    clearInterval(this.intervalId)
  },
  watch: {
    currentEspSettings(values) {
      this.currentSettings = values.data
    },
  },
}
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->

<style>
</style>
