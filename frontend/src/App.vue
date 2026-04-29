<!-- App.vue -->
<!-- Main component of Fifoz — Fantasy Football Web App -->
<!-- Manages navigation between Home, Players, Tools (Squad Builder + Compare) -->
<!-- Handles authentication state and shows login modal when needed -->

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import HomePage from './components/HomePage.vue'
import PlayerList from './components/PlayerList.vue'
import SquadBuilder from './components/SquadBuilder.vue'
import ComparePlayer from './components/ComparePlayer.vue'
import AuthModal from './components/AuthModal.vue'
import { isLoggedIn, getUsername, logout } from './auth.js'

const players = ref([])
const loading = ref(true)
const activePage = ref('home')
const activeTool = ref('squad')
const showAuthModal = ref(false)
const loggedIn = ref(isLoggedIn())
const username = ref(getUsername())
const pendingPage = ref(null)

onMounted(async () => {
  const response = await axios.get('http://127.0.0.1:8000/api/players/')
  players.value = response.data
  loading.value = false
})

// Navigate to a page
const navigateTo = (page) => {
  if ((page === 'tools' || page === 'squad' || page === 'compare') && !loggedIn.value) {
    pendingPage.value = page
    showAuthModal.value = true
    return
  }
  if (page === 'squad' || page === 'compare') {
    activeTool.value = page
    activePage.value = 'tools'
    return
  }
  activePage.value = page
}

// Called when user successfully logs in or signs up
const onAuthenticated = () => {
  loggedIn.value = true
  username.value = getUsername()
  showAuthModal.value = false
  if (pendingPage.value) {
    navigateTo(pendingPage.value)
    pendingPage.value = null
  }
}

// Logout
const handleLogout = () => {
  logout()
  loggedIn.value = false
  username.value = null
  activePage.value = 'home'
}

const addToSquad = () => {
  navigateTo('squad')
}

// Nav items
const navItems = [
  { label: '🏠 Home', value: 'home' },
  { label: '🏃 Players', value: 'players' },
  { label: '🛠️ Tools', value: 'tools' },
]
</script>

<template>
  <div class="min-h-screen bg-gray-900 text-white">

    <!-- Auth Modal -->
    <AuthModal
      v-if="showAuthModal"
      @authenticated="onAuthenticated"
      @close="showAuthModal = false; pendingPage = null"
    />

    <!-- Header -->
    <div class="bg-gray-800 border-b border-gray-700 px-6 py-4 sticky top-0 z-40">
      <div class="max-w-7xl mx-auto flex justify-between items-center">

        <!-- Logo -->
        <div
          @click="activePage = 'home'"
          class="text-2xl font-black text-green-400 cursor-pointer hover:text-green-300 transition"
        >
          ⚽ Fifoz
        </div>

        <!-- Navigation -->
        <div class="flex gap-2">
          <button
            v-for="item in navItems"
            :key="item.value"
            @click="navigateTo(item.value)"
            :class="activePage === item.value ? 'bg-green-600 border-green-500 text-white' : 'bg-gray-700 border-gray-600 text-gray-300'"
            class="px-4 py-2 rounded-lg border font-bold hover:bg-green-700 hover:text-white transition text-sm"
          >
            {{ item.label }}
            <span v-if="item.value === 'tools' && !loggedIn" class="ml-1">🔒</span>
          </button>
        </div>

        <!-- Auth buttons -->
        <div v-if="loggedIn" class="flex items-center gap-3">
          <span class="text-green-400 text-sm font-bold">👤 {{ username }}</span>
          <button
            @click="handleLogout"
            class="bg-gray-700 hover:bg-gray-600 text-white text-sm px-4 py-2 rounded-lg transition"
          >
            Logout
          </button>
        </div>
        <div v-else class="flex gap-2">
          <button
            @click="showAuthModal = true"
            class="bg-gray-700 hover:bg-gray-600 text-white text-sm px-4 py-2 rounded-lg transition"
          >
            Login
          </button>
          <button
            @click="showAuthModal = true"
            class="bg-green-600 hover:bg-green-500 text-white text-sm px-4 py-2 rounded-lg transition"
          >
            Sign Up
          </button>
        </div>
      </div>
    </div>

    <!-- Main content -->
    <div class="max-w-7xl mx-auto p-6">
      <div v-if="loading" class="text-center text-gray-400 mt-20">
        <div class="text-4xl mb-4">⚽</div>
        Loading Fifoz...
      </div>

      <div v-else>
        <!-- Home Page -->
        <HomePage
          v-if="activePage === 'home'"
          :players="players"
          :onAdd="addToSquad"
          :onNavigate="navigateTo"
        />

        <!-- Players Page -->
        <PlayerList
          v-if="activePage === 'players'"
          :players="players"
          :onAdd="addToSquad"
        />

        <!-- Tools Page -->
        <div v-if="activePage === 'tools'">
          <!-- Tools navigation -->
          <div class="flex gap-3 mb-6">
            <button
              @click="activeTool = 'squad'"
              :class="activeTool === 'squad' ? 'bg-green-600 border-green-500' : 'bg-gray-800 border-gray-700'"
              class="px-5 py-2 rounded-lg border font-bold hover:bg-green-700 transition"
            >
              🏟️ Squad Builder
            </button>
            <button
              @click="activeTool = 'compare'"
              :class="activeTool === 'compare' ? 'bg-green-600 border-green-500' : 'bg-gray-800 border-gray-700'"
              class="px-5 py-2 rounded-lg border font-bold hover:bg-green-700 transition"
            >
              ⚔️ Compare Players
            </button>
          </div>

          <SquadBuilder
            v-if="activeTool === 'squad'"
            :players="players"
          />
          <ComparePlayer
            v-if="activeTool === 'compare'"
            :players="players"
          />
        </div>
      </div>
    </div>
  </div>
</template>