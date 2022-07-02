import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'

Vue.use(Router)

/* eslint-disable */
let router = new Router({
mode: 'history',
routes: [
    {
        path: '/',
        name: 'home',
        component: Home
    },
    ]
})

export default router
