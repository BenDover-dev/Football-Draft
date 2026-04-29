<!-- PlayerList.vue -->
<!-- Displays the full list of players with search, position filters -->
<!-- and sort options. Uses PlayerCard component for each player. -->
<!-- Follows DRY principle — search, filter and sort logic all in one place -->

<script setup>
import { ref, computed } from 'vue'
import PlayerCard from './PlayerCard.vue'

// Props received from parent
const props = defineProps({
  players: Array,   // Full list of players from API
  onAdd: Function,  // Function to call when a player is added to squad
})

const search = ref('')
const selectedPosition = ref('ALL')
const sortBy = ref('draft_score')

// Normalize text for accent-insensitive search
// e.g. searching "Estevao" will find "Estêvão"
const normalize = (str) => str.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase()

const filteredPlayers = computed(() => {
  let result = props.players.filter(player => {
    const matchesSearch = normalize(player.name).includes(normalize(search.value))
    const matchesPosition = selectedPosition.value === 'ALL' || player.position === selectedPosition.value
    return matchesSearch && matchesPosition
  })
  result.sort((a, b) => b[sortBy.value] - a[sortBy.value])
  return result
})
</script>

<template>
  <div>
    <!-- Search and position filters -->
    <div class="flex flex-col md:flex-row gap-4 mb-4">
      <input
        v-model="search"
        type="text"
        placeholder="Search players..."
        class="flex-1 bg-gray-800 text-white border border-gray-700 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500"
      />
      <div class="flex gap-2">
        <button
          v-for="pos in ['ALL', 'GK', 'DEF', 'MID', 'FWD']"
          :key="pos"
          @click="selectedPosition = pos"
          :class="selectedPosition === pos ? 'bg-blue-600' : 'bg-gray-800'"
          class="px-4 py-2 rounded-lg border border-gray-700 hover:bg-blue-700 transition"
        >
          {{ pos }}
        </button>
      </div>
    </div>

    <!-- Sort options -->
    <div class="flex gap-2 mb-6">
      <span class="text-gray-400 self-center">Sort by:</span>
      <button
        v-for="sort in [
          { label: 'Draft Score', value: 'draft_score' },
          { label: 'Form', value: 'form' },
          { label: 'Points', value: 'total_points' },
          { label: 'Price', value: 'price' },
        ]"
        :key="sort.value"
        @click="sortBy = sort.value"
        :class="sortBy === sort.value ? 'bg-green-600' : 'bg-gray-800'"
        class="px-4 py-2 rounded-lg border border-gray-700 hover:bg-green-700 transition"
      >
        {{ sort.label }}
      </button>
    </div>

    <!-- Player cards grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      <PlayerCard
        v-for="player in filteredPlayers"
        :key="player.id"
        :player="player"
        :onAdd="onAdd"
      />
    </div>
  </div>
</template>