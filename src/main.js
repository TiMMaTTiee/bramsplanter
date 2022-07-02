import Vue from 'vue'
import App from './App.vue'
import router from '@/router'
import store from '@/store'

// bootstrap mobile first
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

// graphs
import HighchartsVue from 'highcharts-vue'
import Highcharts from 'highcharts'
import stockInit from 'highcharts/modules/stock'

stockInit(Highcharts)

Vue.use(HighchartsVue)

Vue.use(BootstrapVue)

Vue.config.devtools = true

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
