<template>
  <b-row class="panel">
    <highcharts
      class="bar"
      :options="chartOptions"
      :updateArgs="updateArgs"
    ></highcharts>
  </b-row>
</template>

<script>
/* eslint-disable */
/* eslint-disable no-console */
import { mapState, mapActions } from 'vuex'

export default {
  name: 'CellsView',
  data() {
    return {
      graphName: 'Battery voltage',
      graphDetail: 'Cell voltage over time per ',
      timeType: 'hour',
      timeCount: 5,
      xAxisValues: [],
      monthNames: [
        'Jan',
        'Feb',
        'Mar',
        'Apr',
        'May',
        'Jun',
        'Jul',
        'Aug',
        'Sep',
        'Oct',
        'Nov',
        'Dec',
      ],
      updateArgs: [true, true, { duration: 1000 }],
      series: null,
      cellData: null,
    }
  },
  methods: {
    setAxisValues() {
      this.xAxisValues = []
      if (this.timeType == 'hour') {
        for (var i = this.series[0].data.length - 1; i > -1; i--) {
          var today = new Date()
          today.setHours(today.getHours() - i)
          this.xAxisValues.push(String(today.getHours()) + ':00')
        }
      }

      if (this.timeType == 'day') {
        for (var i = this.series[0].data.length - 1; i > -1; i--) {
          var today = new Date()
          today.setDate(today.getDate() - i)
          this.xAxisValues.push(
            String(today.getDate()) + ' ' + this.monthNames[today.getMonth()],
          )
        }
      }

      if (this.timeType == 'week') {
        for (var i = this.series[0].data.length - 1; i > -1; i--) {
          var today = new Date()
          today.setDate(today.getDate() - i)
          var then = new Date()
          then.setDate(then.getDate() - (i + 7))
          this.xAxisValues.push(
            String(then.getDate()) +
              ' ' +
              this.monthNames[then.getMonth()] +
              ' - ' +
              String(today.getDate()) +
              ' ' +
              this.monthNames[today.getMonth()],
          )
        }
      }

      this.chartOptions.xAxis.categories = this.xAxisValues
    },
  },
  mounted() {
    this.setAxisValues()
  },
  computed: {
    ...mapState({
      currentMoist: (state) => state.data.moist,
      currentCells: (state) => state.data.cells,
      currentTimeType: (state) => state.data.timeType,
      currentTimeCount: (state) => state.data.timeCount,
    }),
    lastTimeType() {
      return this.timeType
    },
    chartOptions() {
      return {
        chart: {
          type: 'line',
        },
        title: {
          text: this.graphName,
        },
        subtitle: {
          text: this.graphDetail + this.lastTimeType,
        },
        xAxis: {
          categories: this.xAxisValues,
        },
        yAxis: {
          title: {
            text: 'Voltage',
          },
          valueSuffix: 'V',
          plotLines: [
            {
              value: 0,
              width: 1,
              color: '#808080',
            },
          ],
        },
        tooltip: {
          valueSuffix: 'V',
        },
        series: this.series,
      }
    },
  },
  watch: {
    currentCells(values) {
      this.cellData = values
    },
    currentMoist(count) {
      this.series = count.cell_data
      this.setAxisValues()
    },
    currentTimeType(type) {
      this.timeType = type
    },
    currentTimeCount(count) {
      this.timeCount = count
    },
  },
}
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->

<style>
</style>
