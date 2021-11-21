<template>
  <b-row class="panel">
    <b-col>
      <h3>Data</h3>
    </b-col>
    <b-col>
      <b-row>
        <b-button-group>
          <b-button @click="newTimeCount(-1)">-</b-button>
          <b-button disabled> {{ timeCount }} </b-button>
          <b-button @click="newTimeCount(+1)">+</b-button>
        </b-button-group>
      </b-row>

      <b-row>
        <b-button-group>
          <b-button @click="newTimeType(-1)">-</b-button>
          <b-button disabled> {{ timeTypes[timeType] }} </b-button>
          <b-button @click="newTimeType(+1)">+</b-button>
        </b-button-group>
      </b-row>
    </b-col>
    <b-col>
      <MoistView />
    </b-col>
  </b-row>
</template>

<script>
/* eslint-disable */
/* eslint-disable no-console */
import { mapState, mapActions } from 'vuex'
import MoistView from './Moist.vue'
import RecentDataView from './RecentData.vue'

export default {
  name: 'PlotView',
  data() {
    return {
      timeTypes: ['hour', 'day', 'week'],
      timeType: 0,
      timeCount: 5,
    }
  },
  components: {
    MoistView,
    RecentDataView,
  },
  methods: {
    ...mapActions('data', ['setTimeCount', 'setTimeType']),
    newTimeCount(delta) {
      if (this.timeCount + delta > 0) {
        this.timeCount += delta
        this.setTimeCount(this.timeCount)
      }
    },
    newTimeType(delta) {
      if (
        this.timeType + delta > -1 &&
        this.timeType + delta < this.timeTypes.length
      ) {
        this.timeType += delta
        this.setTimeType(this.timeTypes[this.timeType])
      }
    },
  },
  mounted() {},
  computed: {},
  created() {},
  beforeDestroy() {},
  watch: {},
}
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->

<style>
</style>
