<template>
  <b-row class="panel">
    <h3>Settings</h3>

    <b-form @submit.prevent="onSubmit" @reset="onReset" id="form">
      <b-form-group
        label-cols="4"
        label="Trigger pump 1:"
        label-align-lg="left"
        label-for="nested-time"
      >
        <b-form-checkbox
          v-model="form.manualTrigger"
          name="check-button"
          switch
          size="lg"
        >
        </b-form-checkbox>
      </b-form-group>

      <b-form-group
        label-cols="4"
        label="Trigger pump 2:"
        label-align-lg="left"
        label-for="nested-time"
      >
        <b-form-checkbox
          v-model="form.manualTrigger_2"
          name="check-button"
          switch
          size="lg"
        >
        </b-form-checkbox>
      </b-form-group>

      <b-form-group
        label-cols="4"
        label="Water amount for pump 1:"
        label-align-lg="left"
        label-for="nested-start-margin"
      >
        <b-form-spinbutton
          style="width: 60%; float: left"
          v-model="form.manualAmount"
          min="1"
          max="10000"
        ></b-form-spinbutton>
        <p style="width: 30%; float: right">seconds</p>
      </b-form-group>

      <b-form-group
        label-cols="4"
        label="Water amount for pump 2:"
        label-align-lg="left"
        label-for="nested-start-margin"
      >
        <b-form-spinbutton
          style="width: 60%; float: left"
          v-model="form.manualAmount_2"
          min="1"
          max="10000"
        ></b-form-spinbutton>
        <p style="width: 30%; float: right">seconds</p>
      </b-form-group>

      <b-form-group
        label-cols="4"
        label="Minimum water pump 1:"
        label-align-lg="left"
        label-for="nested-start-margin"
      >
        <b-form-spinbutton
          style="width: 60%; float: left"
          v-model="form.limit_1"
          min="1"
          max="10000"
        ></b-form-spinbutton>
        <p style="width: 30%; float: right">%</p>
      </b-form-group>

      <b-form-group
        label-cols="4"
        label="Minimum water pump 2:"
        label-align-lg="left"
        label-for="nested-start-margin"
      >
        <b-form-spinbutton
          style="width: 60%; float: left"
          v-model="form.limit_2"
          min="1"
          max="10000"
        ></b-form-spinbutton>
        <p style="width: 30%; float: right">%</p>
      </b-form-group>

      <b-form-group
        label-cols="4"
        label="Update interval:"
        label-align-lg="left"
        label-for="nested-start-margin"
      >
        <b-form-spinbutton
          style="width: 60%; float: left"
          v-model="form.updateInterval"
          min="1"
          max="10000"
        ></b-form-spinbutton>
        <p style="width: 30%; float: right">seconds</p>
      </b-form-group>

      <b-form-group
        label-cols="6"
        label=""
        label-align-lg="left"
        label-for="nested-size"
      >
        <b-button type="submit" variant="primary" style="margin-right: 1rem"
          >Save</b-button
        >
        <b-button type="reset">Cancel</b-button>
      </b-form-group>
    </b-form>

    <b-modal ok-only v-model="showSendDialog" @ok="resetModal()">
      <div v-if="sending">
        <p>Updating settings...</p>
        <b-spinner label="Spinning"></b-spinner>
      </div>
      <div v-else>
        <p v-if="sendState">Updated settings</p>
        <p v-else>Failed to update settings</p>
      </div>
    </b-modal>
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
      form: {
        manualTrigger: null,
        manualTrigger_2: null,
        manualAmount: null,
        manualAmount_2: null,
        updateInterval: null,
        limit_1: null,
        limit_2: null,
      },
      sending: false,
      sendState: null,
      showSendDialog: false,
    }
  },
  methods: {
    ...mapActions('status', ['getEspSettings', 'setEspSettings']),
    onSubmit() {
      this.sending = true
      this.sendState = null
      this.showSendDialog = true
      var args = [this.$store.state.plots.activePlot.api_key]
      args.push(
        this.form.manualTrigger ? 1 : 0,
        this.form.manualTrigger_2 ? 1 : 0,
        this.form.manualAmount,
        this.form.manualAmount_2,
        this.form.updateInterval,
        this.form.limit_1,
        this.form.limit_2
      )
      this.setEspSettings({ args: args })
    },
    onReset() {},
    resetModal() {
      this.sending = false
      this.sendState = null
      this.showSendDialog = false
      this.$router.go()
    },
  },
  mounted() {},
  computed: {
    ...mapState({
      currentEspSettings: (state) => state.status.espSettings,
      currentSendState: (state) => state.status.sendStatus,
    }),
  },
  created() {
    this.getEspSettings({ args: [this.$store.state.plots.activePlot.api_key] })
  },
  watch: {
    currentEspSettings(values) {
      this.currentSettings = values.data
      this.form.manualTrigger = values.data.manual_trigger ? true : false
      this.form.manualTrigger_2 = values.data.manual_trigger_2 ? true : false
      this.form.manualAmount = values.data.manual_amount
      this.form.manualAmount_2 = values.data.manual_amount_2
      this.form.updateInterval = values.data.update_interval
      this.form.limit_1 = values.data.limit_1
      this.form.limit_2 = values.data.limit_2
    },
    currentSendState(status) {
      this.sending = false
      this.sendState = status.data
    },
  },
}
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->

<style>
#form {
  width: 40rem;
}
</style>
