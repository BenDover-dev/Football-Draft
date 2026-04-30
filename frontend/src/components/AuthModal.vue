<!-- AuthModal.vue -->
<!-- Login, Signup and Forgot Password modal component. -->
<!-- Toggles between login, signup and forgot password forms. -->
<!-- On success, emits 'authenticated' event to parent component. -->

<script setup>
import { ref } from 'vue'
import { login, register } from '../auth.js'
import axios from 'axios'

const emit = defineEmits(['authenticated', 'close'])

// Mode: 'login', 'signup', 'forgot'
const mode = ref('login')
const username = ref('')
const email = ref('')
const password = ref('')
const error = ref('')
const success = ref('')
const loading = ref(false)

const resetFields = () => {
  username.value = ''
  email.value = ''
  password.value = ''
  error.value = ''
  success.value = ''
}

const switchMode = (newMode) => {
  mode.value = newMode
  resetFields()
}

const handleSubmit = async () => {
  error.value = ''
  success.value = ''
  loading.value = true

  try {
    if (mode.value === 'login') {
      await login(username.value, password.value)
      emit('authenticated')
    } else if (mode.value === 'signup') {
      await register(username.value, email.value, password.value)
      emit('authenticated')
    } else if (mode.value === 'forgot') {
      await axios.post(`${import.meta.env.VITE_API_URL}/api/auth/forgot-password/`, { email: email.value })
      success.value = 'If this email is registered you will receive a reset link shortly!'
    }
  } catch (err) {
    error.value = err.response?.data?.error || 'Something went wrong. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <!-- Backdrop -->
  <div
    class="fixed inset-0 bg-black/70 z-50 flex items-center justify-center"
    @click.self="emit('close')"
  >
    <!-- Modal -->
    <div class="bg-gray-900 border border-gray-700 rounded-2xl p-8 w-full max-w-md mx-4 relative">

      <!-- Close button -->
      <button
        @click="emit('close')"
        class="absolute top-4 right-4 text-gray-400 hover:text-white text-xl"
      >✕</button>

      <!-- Header -->
      <div class="text-center mb-6">
        <div class="text-4xl mb-2">⚽</div>
        <h2 class="text-2xl font-bold text-white">
          {{ mode === 'login' ? 'Welcome Back!' : mode === 'signup' ? 'Create Account' : 'Forgot Password' }}
        </h2>
        <p class="text-gray-400 text-sm mt-1">
          {{ mode === 'login' ? 'Login to access Squad Builder and Compare' : mode === 'signup' ? 'Sign up to start building your squad' : 'Enter your email to receive a reset link' }}
        </p>
      </div>

      <!-- Error message -->
      <div v-if="error" class="bg-red-900/50 border border-red-700 text-red-300 rounded-lg px-4 py-3 mb-4 text-sm">
        {{ error }}
      </div>

      <!-- Success message -->
      <div v-if="success" class="bg-green-900/50 border border-green-700 text-green-300 rounded-lg px-4 py-3 mb-4 text-sm">
        {{ success }}
      </div>

      <!-- Form -->
      <div class="flex flex-col gap-4">

        <!-- Username (login and signup only) -->
        <div v-if="mode !== 'forgot'">
          <label class="text-gray-400 text-xs mb-1 block">Username</label>
          <input
            v-model="username"
            type="text"
            placeholder="Enter your username"
            class="w-full bg-gray-800 text-white border border-gray-700 rounded-lg px-4 py-3 focus:outline-none focus:border-green-500 transition"
          />
        </div>

        <!-- Email (signup and forgot only) -->
        <div v-if="mode === 'signup' || mode === 'forgot'">
          <label class="text-gray-400 text-xs mb-1 block">Email</label>
          <input
            v-model="email"
            type="email"
            placeholder="Enter your email"
            class="w-full bg-gray-800 text-white border border-gray-700 rounded-lg px-4 py-3 focus:outline-none focus:border-green-500 transition"
          />
        </div>

        <!-- Password (login and signup only) -->
        <div v-if="mode !== 'forgot'">
          <label class="text-gray-400 text-xs mb-1 block">Password</label>
          <input
            v-model="password"
            type="password"
            placeholder="Enter your password"
            class="w-full bg-gray-800 text-white border border-gray-700 rounded-lg px-4 py-3 focus:outline-none focus:border-green-500 transition"
            @keyup.enter="handleSubmit"
          />
        </div>

        <!-- Forgot password link (login only) -->
        <div v-if="mode === 'login'" class="text-right">
          <button
            @click="switchMode('forgot')"
            class="text-green-400 hover:text-green-300 text-xs"
          >
            Forgot Password?
          </button>
        </div>

        <!-- Submit button -->
        <button
          @click="handleSubmit"
          :disabled="loading"
          class="w-full bg-green-600 hover:bg-green-500 disabled:bg-gray-700 text-white font-bold py-3 rounded-lg transition mt-2"
        >
          {{ loading ? 'Please wait...' : mode === 'login' ? 'Login' : mode === 'signup' ? 'Create Account' : 'Send Reset Link' }}
        </button>
      </div>

      <!-- Toggle between modes -->
      <div class="text-center mt-6 text-sm text-gray-400">
        <span v-if="mode === 'login'">
          Don't have an account?
          <button @click="switchMode('signup')" class="text-green-400 hover:text-green-300 font-bold ml-1">Sign Up</button>
        </span>
        <span v-else-if="mode === 'signup'">
          Already have an account?
          <button @click="switchMode('login')" class="text-green-400 hover:text-green-300 font-bold ml-1">Login</button>
        </span>
        <span v-else>
          Remember your password?
          <button @click="switchMode('login')" class="text-green-400 hover:text-green-300 font-bold ml-1">Login</button>
        </span>
      </div>

    </div>
  </div>
</template>