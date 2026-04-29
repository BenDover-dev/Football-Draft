<!-- HomePage.vue -->
<!-- Fifoz home page component. -->
<!-- Shows hero banner, featured players, latest news and recent scores. -->
<!-- Follows RenderZ style layout with dark theme. -->

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import PlayerCard from './PlayerCard.vue'

const props = defineProps({
  players: Array,
  onAdd: Function,
  onNavigate: Function,
})

const news = ref([])
const loadingNews = ref(true)

// Get top 8 players by draft score for featured section
const featuredPlayers = computed(() => {
  return [...props.players]
    .sort((a, b) => b.draft_score - a.draft_score)
    .slice(0, 8)
})

onMounted(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/auth/news/')
    news.value = response.data.articles || []
  } catch (err) {
    console.error('Failed to fetch news:', err)
  } finally {
    loadingNews.value = false
  }
})

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })
}
</script>

<template>
  <div class="text-white">

    <!-- Hero Banner -->
    <div class="relative bg-gradient-to-r from-green-900 via-gray-900 to-gray-900 rounded-2xl p-10 mb-10 overflow-hidden">
      <div class="absolute inset-0 opacity-10 text-9xl flex items-center justify-center font-black text-green-400">
        ⚽
      </div>
      <div class="relative z-10">
        <h1 class="text-5xl font-black text-white mb-3">
          Welcome to <span class="text-green-400">Fifoz</span>
        </h1>
        <p class="text-gray-300 text-lg mb-6 max-w-xl">
          Build your dream squad, compare players, and stay up to date with the latest Premier League news and scores.
        </p>
        <div class="flex gap-3">
          <button
            @click="onNavigate('players')"
            class="bg-green-600 hover:bg-green-500 text-white font-bold px-6 py-3 rounded-xl transition"
          >
            🏃 Browse Players
          </button>
          <button
            @click="onNavigate('squad')"
            class="bg-gray-700 hover:bg-gray-600 text-white font-bold px-6 py-3 rounded-xl transition"
          >
            🏟️ Build Squad
          </button>
        </div>
      </div>
    </div>

    <!-- Featured Players -->
    <div class="mb-10">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-2xl font-bold">🌟 Top Rated Players</h2>
        <button
          @click="onNavigate('players')"
          class="text-green-400 hover:text-green-300 text-sm font-bold"
        >
          View All →
        </button>
      </div>
      <div class="overflow-x-auto pb-4">
        <div class="flex gap-4 min-w-max">
          <PlayerCard
            v-for="player in featuredPlayers"
            :key="player.id"
            :player="player"
            :onAdd="onAdd"
          />
        </div>
      </div>
    </div>

    <!-- Latest News -->
    <div class="mb-10">
      <h2 class="text-2xl font-bold mb-4">📰 Latest Football News</h2>

      <div v-if="loadingNews" class="text-gray-400 text-center py-8">
        Loading news...
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        
          v-for="article in news"
          :key="article.url"
          :href="article.url"
          target="_blank"
          class="bg-gray-800 border border-gray-700 rounded-xl overflow-hidden hover:border-green-500 transition cursor-pointer"
        >
          <!-- News image -->
          <div class="h-40 bg-gray-700 overflow-hidden">
            <img
              v-if="article.urlToImage"
              :src="article.urlToImage"
              :alt="article.title"
              class="w-full h-full object-cover"
              @error="$event.target.style.display='none'"
            />
            <div v-else class="w-full h-full flex items-center justify-center text-4xl">
              ⚽
            </div>
          </div>

          <!-- News content -->
          <div class="p-4">
            <div class="text-xs text-green-400 mb-1 font-bold">
              {{ article.source?.name || 'Football News' }}
            </div>
            <h3 class="text-sm font-bold text-white mb-2 line-clamp-2">
              {{ article.title }}
            </h3>
            <p class="text-xs text-gray-400 line-clamp-2 mb-3">
              {{ article.description }}
            </p>
            <div class="text-xs text-gray-500">
              {{ formatDate(article.publishedAt) }}
            </div>
          </div>
        </a>
      </div>
    </div>

  </div>
</template>