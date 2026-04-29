// main.js
// Entry point of the Vue frontend application.
// Mounts the app to the DOM and registers the router.

import { createApp } from 'vue'
import './style.css'
import RouterApp from './RouterApp.vue'
import router from './router.js'

const app = createApp(RouterApp)
app.use(router)
app.mount('#app')