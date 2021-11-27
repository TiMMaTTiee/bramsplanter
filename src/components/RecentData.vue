<template>
  <b-row class="panel">
    <h3>Latest data</h3>
    <b-alert show v-for="(field, id) in fields" v-bind:key="id.id">
      <b-col cols="8"> {{ field['label'] }}: </b-col>
      <b-col cols="4">
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
        <b-badge v-else-if="field['key'] == 'timestamp'" variant="primary"
          >{{ recentData[field['key']] }}
        </b-badge>
        <b-badge v-else variant="primary"
          >{{ recentData[field['key']] }}
          %
        </b-badge>
      </b-col>
    </b-alert>
    <b-table striped hover :items="recentDataArray" :fields="fields"></b-table>
    <b-form-checkbox v-model="dumbTempUnit" name="check-button" switch>
      Fahrenheit
    </b-form-checkbox>
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
      recentDataArray: [],
      recentImage: null,
      dumbTempUnit: false,
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
        { key: 'timestamp', label: 'Timestamp' },
      ],
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
      this.recentDataArray[0] = values.data
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
