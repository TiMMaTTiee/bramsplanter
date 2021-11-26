<template>
  <b-row class="panel">
    <b-col cols="8">
      <highcharts
        class="bar"
        :options="chartOptions"
        :updateArgs="updateArgs"
      ></highcharts>
    </b-col>
    <b-col cols="4">
      {{ cellData }}
    </b-col>
  </b-row>
</template>

<script>
/* eslint-disable */
/* eslint-disable no-console */
import { mapState, mapActions } from 'vuex'

export default {
  name: 'MoistView',
  data() {
    return {
      graphName: 'Humidity',
      graphDetail: 'Humidity over time per ',
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
      series: [
        {
          data: [34, 32, 33, 36, 39, 34, 36],
          name: 'Plot 1',
        },
        {
          data: [46, 41, 48, 39, 39, 41, 46],
          name: 'Plot 2',
        },
        {
          data: [30, 31, 31, 33, 33, 28, 31],
          name: 'Plot 3',
        },
      ],
      cellData: null,
    }
  },
  methods: {
    ...mapActions('data', ['getMoist', 'getCells']),
    setAxisValues() {
      this.xAxisValues = []

      if (this.timeType == 'hour') {
        for (var i = this.timeCount - 1; i > -1; i--) {
          var today = new Date()
          today.setHours(today.getHours() - i)
          this.xAxisValues.push(String(today.getHours()) + ':00')
        }
      }

      if (this.timeType == 'day') {
        for (var i = this.timeCount - 1; i > -1; i--) {
          var today = new Date()
          today.setDate(today.getDate() - i)
          this.xAxisValues.push(
            String(today.getDate()) + ' ' + this.monthNames[today.getMonth()],
          )
        }
      }

      if (this.timeType == 'week') {
        for (var i = this.timeCount - 1; i > -1; i--) {
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
            text: 'Percentage',
          },
          valueSuffix: '%',
          plotLines: [
            {
              value: 0,
              width: 1,
              color: '#808080',
            },
          ],
        },
        tooltip: {
          valueSuffix: '%',
        },
        series: this.series,
      }
    },
  },
  created() {
    // this.getMoist({ args: [1, this.timeType, this.timeCount] })
    this.getMoist({ args: [this.$store.state.auth.user.uuid] })
    this.getCells({ args: [this.$store.state.auth.user.uuid] })
    this.intervalId = setInterval(() => {
      // this.getMoist({ args: [1, this.timeType, this.timeCount] })
      this.getCells({ args: [this.$store.state.auth.user.uuid] })
      this.getMoist({ args: [this.$store.state.auth.user.uuid] })
    }, 10000)
  },
  beforeDestroy() {
    clearInterval(this.intervalId)
  },
  watch: {
    currentCells(values) {
      this.cellData = values
    },
    currentMoist(count) {
      console.log(count.data)
      this.series[0] = count.data
      // Create an array of dictionaries to enter as new data
      // var series = []
      // this.series = []
      // count.data.forEach((element) => {
      //   for (var key in element) {
      //     // check if key already exists
      //     var exists = false
      //     series.forEach((existingElement) => {
      //       if (existingElement[key]) {
      //         existingElement[key].push(element[key])
      //         exists = true
      //       }
      //     })

      //     // if the key does not yet exists, add as new key
      //     if (!exists) {
      //       var newEntry = { [key]: [element[key]] }
      //       series.push(newEntry)
      //     }
      //   }
      // })

      // // add data to the chart
      // series.forEach((element) => {
      //   for (var key in element) {
      //     this.series.push({
      //       name: key,
      //       data: element[key],
      //     })
      //   }
      // })
      this.setAxisValues()
    },
    currentTimeType(type) {
      this.timeType = type
      this.getMoist({ args: [1, this.timeType, this.timeCount] })
    },
    currentTimeCount(count) {
      console.log(count)
      this.timeCount = count
      this.getMoist({ args: [1, this.timeType, this.timeCount] })
    },
  },
}
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->

<style>
</style>
