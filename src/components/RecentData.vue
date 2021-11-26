<template>
  <b-row class="panel">
    <b-col cols="6">
      <li v-for="(value, name) in recentData" v-bind:key="value.id">
        <div v-if="name == 'cell1' || name == 'cell2' || name == 'cell3'">
          {{ name }}: {{ Math.round(value * 0.1875 * 0.001 * 100) / 100 }} V
        </div>
        <div
          v-else-if="
            name == 'soil_temp1' ||
            name == 'soil_temp2' ||
            name == 'air_temp1' ||
            name == 'air_temp2'
          "
        >
          {{ name }}: {{ value }} C
        </div>
        <div v-else>{{ name }}: {{ value }} %</div>
      </li>
    </b-col>
    <b-col cols="6">
      <img :src="'data:image/png;base64,' + recentImage" />
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
      recentImage: null,
    }
  },
  methods: {
    ...mapActions('data', ['getRecent', 'getRecentImage']),
  },
  mounted() {},
  computed: {
    ...mapState({
      currentRecent: (state) => state.data.recent,
      currentRecentImage: (state) => state.data.recentImage,
    }),
  },
  created() {
    this.getRecent({ args: [this.$store.state.auth.user.uuid] })
    this.getRecentImage({ args: [this.$store.state.auth.user.uuid] })
    this.intervalId = setInterval(() => {
      this.getRecent({ args: [this.$store.state.auth.user.uuid] })
      this.getRecentImage({ args: [this.$store.state.auth.user.uuid] })
    }, 10000)
  },
  beforeDestroy() {
    clearInterval(this.intervalId)
  },
  watch: {
    currentRecent(values) {
      this.recentData = values.data
    },
    currentRecentImage(values) {
      this.recentImage = values.data
    },
  },
}
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->

<style>
</style>
