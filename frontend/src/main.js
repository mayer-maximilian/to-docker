import Vue from 'vue'
import VueRouter from 'vue-router'
import navbar from '@/NavBar.vue'
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import ToggleButton from 'vue-js-toggle-button'
import {BootstrapVue, IconsPlugin } from 'bootstrap-vue'

// Import Bootstrap and BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

// Make BootstrapVue available throughout your project
Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
Vue.use(VueRouter)
Vue.use(ToggleButton)

Vue.config.productionTip = false


import Home from './App.vue'
import Login from './admin/Login.vue'
import AdminPage from './admin/AdminPage'

const routes = [
  { path: '/', component: Home, name: 'home' },
  { path: '/login', component: Login, name: 'login' },
  { path: '/admin', component: AdminPage, name: 'admin'}
]

const router = new VueRouter({
  routes // short for `routes: routes`
})

export const eventBus = new Vue();

new Vue({
  router,
  components: {
    navbar
  }
}).$mount('#app')

