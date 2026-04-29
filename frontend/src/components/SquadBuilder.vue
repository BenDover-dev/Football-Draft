<!-- SquadBuilder.vue -->
<!-- Allows users to build a squad by picking players for each position. -->
<!-- Supports multiple formations and tracks budget spending. -->
<!-- Budget is set at £100m following FPL rules. -->

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  players: Array,  // Full list of players from API
})

// Available formations
const formations = {
  '4-3-3': { GK: 1, DEF: 4, MID: 3, FWD: 3 },
  '4-4-2': { GK: 1, DEF: 4, MID: 4, FWD: 2 },
  '4-2-3-1': { GK: 1, DEF: 4, MID: 5, FWD: 1 },
  '3-5-2': { GK: 1, DEF: 3, MID: 5, FWD: 2 },
}

const selectedFormation = ref('4-3-3')
const budget = ref(100)
const squad = ref([])
const activePosition = ref(null)
const search = ref('')

// Normalize text for accent-insensitive search
const normalize = (str) => str.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase()

// Get slots for current formation
const slots = computed(() => {
  const f = formations[selectedFormation.value]
  const result = []
  for (const [pos, count] of Object.entries(f)) {
    for (let i = 0; i < count; i++) {
      result.push({ position: pos, index: i })
    }
  }
  return result
})

// Remaining budget
const remainingBudget = computed(() => {
  const spent = squad.value.reduce((sum, p) => sum + (p ? p.price : 0), 0)
  return (budget.value - spent).toFixed(1)
})

// Filter players for active position search
const filteredPlayers = computed(() => {
  if (!activePosition.value) return []
  return props.players
    .filter(p => {
      const matchesPosition = p.position === activePosition.value.position
      const matchesSearch = normalize(p.name).includes(normalize(search.value))
      const notInSquad = !squad.value.find(s => s && s.id === p.id)
      return matchesPosition && matchesSearch && notInSquad
    })
    .sort((a, b) => b.draft_score - a.draft_score)
    .slice(0, 8)
})

// Get player in a specific slot
const getPlayerInSlot = (position, index) => {
  const slotIndex = slots.value.findIndex(s => s.position === position && s.index === index)
  return squad.value[slotIndex] || null
}

// Select a slot to fill
const selectSlot = (position, index) => {
  activePosition.value = { position, index }
  search.value = ''
}

// Add player to selected slot
const addPlayerToSlot = (player) => {
  if (!activePosition.value) return
  if (player.price > parseFloat(remainingBudget.value) + (getPlayerInSlot(activePosition.value.position, activePosition.value.index)?.price || 0)) {
    alert('Not enough budget!')
    return
  }
  const slotIndex = slots.value.findIndex(s => s.position === activePosition.value.position && s.index === activePosition.value.index)
  squad.value[slotIndex] = player
  activePosition.value = null
  search.value = ''
}

// Remove player from slot
const removePlayer = (position, index) => {
  const slotIndex = slots.value.findIndex(s => s.position === position && s.index === index)
  squad.value[slotIndex] = null
}

// Position colors
const positionColor = {
  GK: 'border-yellow-400 bg-yellow-900/30',
  DEF: 'border-blue-400 bg-blue-900/30',
  MID: 'border-green-400 bg-green-900/30',
  FWD: 'border-red-400 bg-red-900/30',
}
</script>

<template>
  <div class="text-white">
    <h2 class="text-2xl font-bold mb-6 text-center">Squad Builder</h2>

    <!-- Formation selector and budget -->
    <div class="flex flex-col md:flex-row justify-between items-center gap-4 mb-6">
      <div class="flex gap-2">
        <button
          v-for="(f, name) in formations"
          :key="name"
          @click="selectedFormation = name; squad = []"
          :class="selectedFormation === name ? 'bg-green-600' : 'bg-gray-800'"
          class="px-4 py-2 rounded-lg border border-gray-700 hover:bg-green-700 transition text-sm font-bold"
        >
          {{ name }}
        </button>
      </div>
      <div class="text-lg font-bold">
        Budget: 
        <span :class="remainingBudget < 0 ? 'text-red-400' : 'text-green-400'">
          £{{ remainingBudget }}m
        </span>
        <span class="text-gray-400"> / £100m</span>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Squad slots -->
      <div class="bg-green-900/20 border border-green-800 rounded-xl p-4">
        <div v-for="pos in ['GK', 'DEF', 'MID', 'FWD']" :key="pos" class="mb-4">
          <div class="text-xs text-gray-400 mb-2 font-bold">{{ pos }}</div>
          <div class="flex flex-wrap gap-2">
            <div
              v-for="i in formations[selectedFormation][pos]"
              :key="`${pos}-${i}`"
              @click="selectSlot(pos, i - 1)"
              :class="`${positionColor[pos]} border-2 rounded-lg p-2 cursor-pointer hover:opacity-80 transition min-w-[120px] flex-1`"
            >
              <div v-if="getPlayerInSlot(pos, i - 1)" class="flex items-center gap-2">
                <img
                  :src="`https://resources.premierleague.com/premierleague/photos/players/110x140/p${getPlayerInSlot(pos, i-1).photo}.png`"
                  class="w-8 h-10 object-cover rounded bg-gray-700"
                  @error="$event.target.src='https://resources.premierleague.com/premierleague/photos/players/110x140/Photo-Missing.png'"
                />
                <div class="flex-1 min-w-0">
                  <div class="text-xs font-bold truncate">{{ getPlayerInSlot(pos, i-1).name }}</div>
                  <div class="text-xs text-gray-400">£{{ getPlayerInSlot(pos, i-1).price }}m</div>
                </div>
                <button
                  @click.stop="removePlayer(pos, i - 1)"
                  class="text-red-400 hover:text-red-300 text-xs font-bold"
                >✕</button>
              </div>
              <div v-else class="text-center text-gray-500 text-xs py-1">
                + {{ pos }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Player picker -->
      <div>
        <div v-if="activePosition" class="mb-4">
          <p class="text-sm text-gray-400 mb-2">
            Selecting: <span class="text-white font-bold">{{ activePosition.position }}</span>
          </p>
          <input
            v-model="search"
            type="text"
            :placeholder="`Search ${activePosition.position}...`"
            class="w-full bg-gray-800 text-white border border-gray-700 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500 mb-3"
          />
          <div class="flex flex-col gap-2">
            <div
              v-for="player in filteredPlayers"
              :key="player.id"
              @click="addPlayerToSlot(player)"
              class="flex items-center gap-3 bg-gray-800 hover:bg-gray-700 rounded-lg p-2 cursor-pointer transition"
            >
              <img
                :src="`https://resources.premierleague.com/premierleague/photos/players/110x140/p${player.photo}.png`"
                class="w-8 h-10 object-cover rounded bg-gray-700"
                @error="$event.target.src='https://resources.premierleague.com/premierleague/photos/players/110x140/Photo-Missing.png'"
              />
              <div class="flex-1">
                <div class="text-sm font-bold">{{ player.name }}</div>
                <div class="text-xs text-gray-400">{{ player.team }}</div>
              </div>
              <div class="text-right">
                <div class="text-yellow-400 text-xs font-bold">£{{ player.price }}m</div>
                <div class="text-green-400 text-xs">⭐ {{ player.draft_score }}</div>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="text-center text-gray-400 mt-8">
          Click a position slot on the left to pick a player!
        </div>
      </div>
    </div>
  </div>
</template>