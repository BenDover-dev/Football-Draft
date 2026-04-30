<!-- ResetPassword.vue -->
<!-- Password reset page component. -->
<!-- Users land here after clicking the reset link in their email. -->
<!-- Reads uid and token from URL, sends new password to Django. -->

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const password = ref('')
const confirmPassword = ref('')
const error = ref('')
const success = ref('')
const loading = ref(false)
const uid = ref('')
const token = ref('')

onMounted(() => {
  // Get uid and token from URL
  const params = new URLSearchParams(window.location.search)
  uid.value = params.get('uid')
  token.value = params.get('token')
})

const handleReset = async () => {
  error.value = ''
  success.value = ''

  if (!password.value || !confirmPassword.value) {
    error.value = 'Please fill in both fields'
    return
  }

  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match'
    return
  }

  if (password.value.length < 8) {
    error.value = 'Password must be at least 8 characters'
    return
  }

  loading.value = true

  try {
    await axios.post(`${import.meta.env.VITE_API_URL}/api/auth/reset-password/`, {
      uid: uid.value,
      token: token.value,
      password: password.value,
    })
    success.value = 'Password reset successfully! You can now login.'
    setTimeout(() => {
      window.location.href = '/'
    }, 2000)
  } catch (err) {
    error.value = err.response?.data?.error || 'Something went wrong. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-gray-900 flex items-center justify-center p-4">
    <div class="bg-gray-800 border border-gray-700 rounded-2xl p-8 w-full max-w-md">

      <div class="text-center mb-6">
        <div class="text-4xl mb-2">🔑</div>
        <h2 class="text-2xl font-bold text-white">Reset Password</h2>
        <p class="text-gray-400 text-sm mt-1">Enter your new password below</p>
      </div>

      <!-- Error -->
      <div v-if="error" class="bg-red-900/50 border border-red-700 text-red-300 rounded-lg px-4 py-3 mb-4 text-sm">
        {{ error }}
      </div>

      <!-- Success -->
      <div v-if="success" class="bg-green-900/50 border border-green-700 text-green-300 rounded-lg px-4 py-3 mb-4 text-sm">
        {{ success }}
      </div>

      <div class="flex flex-col gap-4">
        <div>
          <label class="text-gray-400 text-xs mb-1 block">New Password</label>
          <input
            v-model="password"
            type="password"
            placeholder="Enter new password"
            class="w-full bg-gray-700 text-white border border-gray-600 rounded-lg px-4 py-3 focus:outline-none focus:border-green-500 transition"
          />
        </div>

        <div>
          <label class="text-gray-400 text-xs mb-1 block">Confirm Password</label>
          <input
            v-model="confirmPassword"
            type="password"
            placeholder="Confirm new password"
            class="w-full bg-gray-700 text-white border border-gray-600 rounded-lg px-4 py-3 focus:outline-none focus:border-green-500 transition"
            @keyup.enter="handleReset"
          />
        </div>

        <button
          @click="handleReset"
          :disabled="loading"
          class="w-full bg-green-600 hover:bg-green-500 disabled:bg-gray-700 text-white font-bold py-3 rounded-lg transition mt-2"
        >
          {{ loading ? 'Please wait...' : 'Reset Password' }}
        </button>

        <div class="text-center">
          <a href="/" class="text-green-400 hover:text-green-300 text-sm">Back to Home</a>
        </div>
      </div>
    </div>
  </div>
</template>