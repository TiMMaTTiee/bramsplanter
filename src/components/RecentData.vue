<template>
  <b-row class="panel">
    <b-col cols="12">
      <li v-for="(value, name) in recentData" v-bind:key="value.id">
        {{ name }}: {{ Math.round(value * 0.1875 * 0.001 * 100) / 100 }} V
      </li>
    </b-col>
  </b-row>
</template>

<script>
/* eslint-disable */
/* eslint-disable no-console */
import { mapState, mapActions } from 'vuex'

export default {
  name: 'RecentDataView',
  data() {
    return {
      recentData: null,
    }
  },
  methods: {
    ...mapActions('data', ['getRecent']),
  },
  mounted() {},
  computed: {
    ...mapState({
      currentRecent: (state) => state.data.recent,
    }),
  },
  created() {
    this.getRecent({ args: [this.$store.state.auth.user.uuid] })
    this.intervalId = setInterval(() => {
      this.getRecent({ args: [this.$store.state.auth.user.uuid] })
    }, 10000)
  },
  beforeDestroy() {
    clearInterval(this.intervalId)
  },
  watch: {
    currentRecent(values) {
      this.recentData = values.data
    },
  },
}
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->

<style>
</style>
