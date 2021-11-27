<template>
  <b-row class="panel">
    <b-col>
      <h3>Data</h3>
    </b-col>
    <b-col>
      <b-row>
        <b-button-group>
          <b-button @click="newTimeCount(-2)">-</b-button>
          <b-button disabled> {{ timeCount }} </b-button>
          <b-button @click="newTimeCount(+2)">+</b-button>
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
    <b-col>
      <CellsView />
    </b-col>
  </b-row>
</template>

<script>
/* eslint-disable */
/* eslint-disable no-console */
import { mapState, mapActions } from 'vuex'
import MoistView from './Moist.vue'
import CellsView from './Cells.vue'
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
    CellsView,
    RecentDataView,
  },
  methods: {
    ...mapActions('data', ['setTimeCount', 'setTimeType']),
    ...mapActions('data', ['getMoist']),

    newTimeCount(delta) {
      if (this.timeCount + delta > 0) {
        this.timeCount += delta
        this.setTimeCount(this.timeCount)
      }

      this.getMoist({
        args: [
          this.$store.state.auth.user.uuid,
          this.timeTypes[this.timeType],
          this.timeCount,
        ],
      })
    },
    newTimeType(delta) {
      if (
        this.timeType + delta > -1 &&
        this.timeType + delta < this.timeTypes.length
      ) {
        this.timeType += delta
        this.setTimeType(this.timeTypes[this.timeType])
      }

      this.getMoist({
        args: [
          this.$store.state.auth.user.uuid,
          this.timeTypes[this.timeType],
          this.timeCount,
        ],
      })
    },
  },
  mounted() {},
  computed: {},
  created() {
    this.getMoist({
      args: [
        this.$store.state.auth.user.uuid,
        this.timeTypes[this.timeType],
        this.timeCount,
      ],
    })
    this.intervalId = setInterval(() => {
      this.getMoist({
        args: [
          this.$store.state.auth.user.uuid,
          this.timeTypes[this.timeType],
          this.timeCount,
        ],
      })
    }, 10000)
  },
  beforeDestroy() {
    clearInterval(this.intervalId)
  },
  beforeDestroy() {},
  watch: {},
}
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->

<style>
</style>
