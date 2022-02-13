<template>
  <b-row class="panel">
    <h3>Latest data</h3>
    <div
      v-for="(field, id) in getActiveFields"
      v-bind:key="id.id"
      class="data-block"
    >
      <b-alert show>
        {{ field['label'] }}
        <b-badge
          v-if="
            field['key'] == 'cell1' ||
            field['key'] == 'cell2' ||
            field['key'] == 'cell3'
          "
          variant="primary"
          >{{
            Math.round(recentData[field['key']] * 0.1875 * 0.001 * 100) / 100
          }}
          V
        </b-badge>
        <b-badge
          v-else-if="
            field['key'] == 'soil_temp1' ||
            field['key'] == 'soil_temp2' ||
            field['key'] == 'air_temp1' ||
            field['key'] == 'air_temp2'
          "
          variant="primary"
          ><div v-if="dumbTempUnit">
            {{ Math.round(recentData[field['key']] * 1.8) + 32 }} F
          </div>
          <div v-else>{{ recentData[field['key']] }} C</div>
        </b-badge>
        <b-badge v-else-if="field['key'] == 'latest_update'" variant="primary">
          {{ getTimezoned(recentData[field['key']]) }}
        </b-badge>
        <b-badge v-else-if="field['key'] == 'solar_bool'" variant="primary">
          <div v-if="recentData[field['key']] == 0">True</div>
          <div v-else>False</div>
        </b-badge>
        <b-badge v-else variant="primary"
          >{{ recentData[field['key']] }}
          %
        </b-badge>
      </b-alert>
    </div>
    <b-form-checkbox
      style="margin-right: 2rem"
      v-model="dumbTempUnit"
      name="check-button"
      switch
      size="lg"
    >
      <p v-if="dumbTempUnit">Fahrenheit</p>
      <p v-else>Celcius</p>
    </b-form-checkbox>
    <b-form-checkbox
      v-model="dumbTimeUnit"
      name="check-button"
      switch
      size="lg"
    >
      <p v-if="dumbTimeUnit">Los Angeles</p>
      <p v-else>Amsterdam</p>
    </b-form-checkbox>
  </b-row>
</template>

<script>
/* eslint-disable */
/* eslint-disable no-console */
import { mapState, mapActions } from 'vuex'
import moment from 'moment-timezone'

export default {
  name: 'RecentDataView',
  data() {
    return {
      recentData: null,
      recentImage: null,
      dumbTempUnit: false,
      dumbTimeUnit: false,
      enabledSensors: [
        'air_moist1',
        'soil_moist2',
        'air_temp1',
        'cell1',
        'cell2',
        'cell3',
        'soil_moist1',
        'soil_temp1',
        'solar_bool',
        'latest_update',
      ],
      fields: [
        { key: 'air_moist1', label: 'Air moisture 1' },
        { key: 'air_moist2', label: 'Air moisture 2' },
        { key: 'air_temp1', label: 'Air temperature 1' },
        { key: 'air_temp2', label: 'Air temperature 2' },
        { key: 'cell1', label: 'Cell 1' },
        { key: 'cell2', label: 'Cell 2' },
        { key: 'cell3', label: 'Cell 3' },
        { key: 'flow_rate', label: 'Flow rate' },
        { key: 'lux', label: 'Lux' },
        { key: 'soil_moist1', label: 'Soil moisture 1' },
        { key: 'soil_moist2', label: 'Soil moisture 2' },
        { key: 'soil_temp1', label: 'Soil temperature 1' },
        { key: 'soil_temp2', label: 'Soil temperature 2' },
        { key: 'solar_bool', label: 'Solar on' },
        { key: 'latest_update', label: 'Latest update' },
      ],
    }
  },
  methods: {
    ...mapActions('data', ['getRecent', 'getRecentImage']),
    getTimezoned(datetime) {
      var london = moment.tz(datetime, 'Europe/London')
      var losAngeles = london.clone().tz('America/Los_Angeles')
      var amsterdam = london.clone().tz('Europe/Amsterdam')
      if (this.dumbTimeUnit) return losAngeles.format('YYYY-MM-DD HH:mm:ss')
      return amsterdam.format('YYYY-MM-DD HH:mm:ss')
    },
  },
  mounted() {},
  computed: {
    ...mapState({
      currentRecent: (state) => state.data.recent,
      currentRecentImage: (state) => state.data.recentImage,
    }),
    getActiveFields() {
      var activeFields = []
      this.fields.forEach((field) => {
        if (this.enabledSensors.includes(field['key'])) activeFields.push(field)
      })
      return activeFields
    },
  },
  created() {
    this.getRecent({ args: [this.$store.state.plots.activePlot.api_key] })
    this.getRecentImage({ args: [this.$store.state.plots.activePlot.api_key] })
    this.intervalId = setInterval(() => {
      this.getRecent({ args: [this.$store.state.plots.activePlot.api_key] })
      this.getRecentImage({ args: [this.$store.state.plots.activePlot.api_key] })
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
.data-block {
  margin-right: 2rem;
  width: 20%;
}
.badge {
  float: right;
}
</style>
