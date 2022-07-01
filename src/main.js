import Vue from 'vue'
import { createApp } from "vue";
import App from './App.vue'
import router from './router'
import store from './store'

// bootstrap mobile first
import BootstrapVue from 'bootstrap-vue-3'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

// graphs
import HighchartsVue from 'highcharts-vue'
import Highcharts from 'highcharts'
import stockInit from 'highcharts/modules/stock'

stockInit(Highcharts)

const app = createApp(App);
app.use(store)
app.use(router)
app.use(HighchartsVue)
app.use(BootstrapVue)
app.mount("#app");
