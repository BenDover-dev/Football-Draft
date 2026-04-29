// router.js
// Sets up Vue Router for page navigation.
// Currently handles the password reset page route.
// Main app is at / and reset password is at /reset-password

import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import ResetPassword from './components/ResetPassword.vue'

const routes = [
    { path: '/', component: App },
    { path: '/reset-password', component: ResetPassword },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router