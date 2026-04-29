<!-- ComparePlayer.vue -->
<!-- RenderZ style player comparison component. -->
<!-- Supports unlimited players with horizontal scrolling. -->
<!-- Green badge = winning stat, Red badge = losing stat -->
<!-- Players can be added and removed dynamically. -->

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  players: Array,
})

// List of selected players for comparison
const selectedPlayers = ref([])
const searches = ref([''])
const openDropdowns = ref([false])

// Normalize text for accent-insensitive search
const normalize = (str) => str.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase()

// Get filtered players for a specific search input
const getFiltered = (index) => {
  const search = searches.value[index]
  if (!search) return props.players.slice(0, 8)
  return props.players
    .filter(p => normalize(p.name).includes(normalize(search)))
    .slice(0, 8)
}

// Add a new empty slot
const addSlot = () => {
  selectedPlayers.value.push(null)
  searches.value.push('')
  openDropdowns.value.push(false)
}

// Select a player for a slot
const selectPlayer = (index, player) => {
  selectedPlayers.value[index] = player
  searches.value[index] = player.name
  openDropdowns.value[index] = false
}

// Remove a player slot
const removeSlot = (index) => {
  selectedPlayers.value.splice(index, 1)
  searches.value.splice(index, 1)
  openDropdowns.value.splice(index, 1)
}

// Toggle dropdown
const toggleDropdown = (index) => {
  openDropdowns.value = openDropdowns.value.map((_, i) => i === index ? !openDropdowns.value[i] : false)
}

// Generate stats
const scale = (value, min, max) => Math.min(Math.max(Math.round(value), min), max)

const getBoost = (player) => {
  const formBoost = Math.min(player.form / 15, 1)
  const pointsBoost = Math.min(player.total_points / 300, 1)
  const priceBoost = Math.min(player.price / 15, 1)
  return (formBoost * 0.4 + pointsBoost * 0.4 + priceBoost * 0.2)
}

const generateStats = (player) => {
  if (!player) return {}
  const boost = getBoost(player)
  const b = boost * 30
  const base = {
    GK:  { PAC: 40, SHO: 15, PAS: 50, DRI: 40, DEF: 75, PHY: 70 },
    DEF: { PAC: 55, SHO: 30, PAS: 55, DRI: 50, DEF: 75, PHY: 70 },
    MID: { PAC: 65, SHO: 55, PAS: 75, DRI: 70, DEF: 50, PHY: 60 },
    FWD: { PAC: 75, SHO: 75, PAS: 60, DRI: 75, DEF: 25, PHY: 65 },
  }
  const pos = base[player.position] || base.MID
  return {
    PAC: scale(pos.PAC + b * 0.8, 30, 99),
    SHO: scale(pos.SHO + b * 0.9, 10, 99),
    PAS: scale(pos.PAS + b * 0.7, 30, 99),
    DRI: scale(pos.DRI + b * 0.8, 30, 99),
    DEF: scale(pos.DEF + b * 0.6, 10, 99),
    PHY: scale(pos.PHY + b * 0.5, 40, 99),
  }
}

// Get best value for a stat across all selected players
const getBestStat = (key) => {
  const values = selectedPlayers.value
    .filter(p => p !== null)
    .map(p => generateStats(p)[key])
  return Math.max(...values)
}

// OVR calculation
const getOVR = (stats, position) => {
  const weights = {
    GK:  { PAC: 0.1, SHO: 0.05, PAS: 0.15, DRI: 0.1, DEF: 0.4, PHY: 0.2 },
    DEF: { PAC: 0.15, SHO: 0.05, PAS: 0.15, DRI: 0.1, DEF: 0.4, PHY: 0.15 },
    MID: { PAC: 0.15, SHO: 0.15, PAS: 0.25, DRI: 0.2, DEF: 0.1, PHY: 0.15 },
    FWD: { PAC: 0.2, SHO: 0.3, PAS: 0.15, DRI: 0.2, DEF: 0.05, PHY: 0.1 },
  }
  const w = weights[position] || weights.MID
  return Math.round(
    stats.PAC * w.PAC + stats.SHO * w.SHO + stats.PAS * w.PAS +
    stats.DRI * w.DRI + stats.DEF * w.DEF + stats.PHY * w.PHY
  )
}

// Card styles
const getTierGradient = (ovr) => {
  if (ovr >= 80) return 'linear-gradient(135deg, #c8a84b 0%, #f5e170 30%, #c8a84b 60%, #8b6914 100%)'
  if (ovr >= 65) return 'linear-gradient(135deg, #8a9bb0 0%, #c8d6e5 30%, #8a9bb0 60%, #4a5568 100%)'
  return 'linear-gradient(135deg, #8b5e3c 0%, #c49a6c 30%, #8b5e3c 60%, #4a2c0a 100%)'
}

const getTierText = (ovr) => {
  if (ovr >= 80) return '#5a3e00'
  if (ovr >= 65) return '#2d3748'
  return '#3d1a00'
}

const getPositionColor = (position) => {
  const colors = { GK: 'text-yellow-400', DEF: 'text-blue-400', MID: 'text-green-400', FWD: 'text-red-400' }
  return colors[position] || 'text-gray-400'
}

const statRows = [
  { label: 'Pace', key: 'PAC' },
  { label: 'Shooting', key: 'SHO' },
  { label: 'Passing', key: 'PAS' },
  { label: 'Dribbling', key: 'DRI' },
  { label: 'Defending', key: 'DEF' },
  { label: 'Physical', key: 'PHY' },
]
</script>

<template>
  <div class="text-white">
    <h2 class="text-2xl font-bold mb-8 text-center">⚔️ Compare Players</h2>

    <!-- Horizontal scrollable player cards row -->
    <div class="overflow-x-auto pb-4">
      <div class="flex gap-4 min-w-max px-2">

        <!-- Existing player slots -->
        <div
          v-for="(player, index) in selectedPlayers"
          :key="index"
          class="flex flex-col items-center gap-2 w-40"
        >
          <!-- Player card -->
          <div v-if="player" class="relative">
            <button
              @click="removeSlot(index)"
              class="absolute -top-2 -left-2 z-10 bg-red-500 hover:bg-red-400 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold"
            >✕</button>

            <div
              class="relative w-36 cursor-pointer"
              style="clip-path: polygon(0 0, 85% 0, 100% 8%, 100% 100%, 0 100%)"
              :style="`background: ${getTierGradient(getOVR(generateStats(player), player.position))}`"
            >
              <div class="absolute top-2 left-2 flex flex-col items-center">
                <span class="text-xl font-black leading-none" :style="`color: ${getTierText(getOVR(generateStats(player), player.position))}`">
                  {{ getOVR(generateStats(player), player.position) }}
                </span>
                <span class="text-xs font-black" :class="getPositionColor(player.position)">
                  {{ player.position }}
                </span>
              </div>
              <div class="flex justify-center pt-2 pb-1">
                <img
                  :src="`https://resources.premierleague.com/premierleague/photos/players/110x140/p${player.photo}.png`"
                  class="w-28 h-32 object-cover object-top"
                  @error="$event.target.src='https://resources.premierleague.com/premierleague/photos/players/110x140/Photo-Missing.png'"
                />
              </div>
              <div class="text-center text-xs font-black px-2 pb-2 truncate" :style="`color: ${getTierText(getOVR(generateStats(player), player.position))}`">
                {{ player.name.split(' ').slice(-1)[0].toUpperCase() }}
              </div>
            </div>

            <div class="text-center mt-2">
              <div class="font-bold text-xs truncate max-w-36">{{ player.name }}</div>
              <div class="text-gray-400 text-xs">{{ getOVR(generateStats(player), player.position) }} · {{ player.position }}</div>
              <div class="text-yellow-400 text-xs">£{{ player.price }}m</div>
            </div>
          </div>

          <!-- Empty slot -->
          <div
            v-else
            class="w-36 h-44 bg-gray-800 border-2 border-dashed border-gray-600 rounded-xl flex flex-col items-center justify-center gap-2 cursor-pointer hover:border-gray-400 transition"
            @click="toggleDropdown(index)"
          >
            <span class="text-3xl text-gray-500">+</span>
            <span class="text-xs text-gray-500">Add player</span>
          </div>

          <!-- Search dropdown -->
          <div class="relative w-40">
            <div
              class="flex items-center bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 cursor-pointer"
              @click="toggleDropdown(index)"
            >
              <input
                v-model="searches[index]"
                type="text"
                placeholder="Search..."
                class="flex-1 bg-transparent text-white text-xs focus:outline-none w-24"
                @click.stop="openDropdowns[index] = true"
              />
              <span class="text-gray-400 ml-1">▾</span>
            </div>
            <div
              v-if="openDropdowns[index]"
              class="absolute z-20 w-48 bg-gray-800 border border-gray-700 rounded-lg mt-1 max-h-48 overflow-y-auto shadow-xl"
            >
              <div
                v-for="p in getFiltered(index)"
                :key="p.id"
                @click="selectPlayer(index, p)"
                class="flex items-center gap-2 px-3 py-2 hover:bg-gray-700 cursor-pointer"
              >
                <img
                  :src="`https://resources.premierleague.com/premierleague/photos/players/110x140/p${p.photo}.png`"
                  class="w-5 h-7 object-cover rounded bg-gray-700"
                  @error="$event.target.src='https://resources.premierleague.com/premierleague/photos/players/110x140/Photo-Missing.png'"
                />
                <div class="flex-1 min-w-0">
                  <div class="text-xs font-bold truncate">{{ p.name }}</div>
                  <div class="text-xs text-gray-400">{{ p.team }}</div>
                </div>
                <span :class="getPositionColor(p.position)" class="text-xs font-bold">{{ p.position }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Add new player slot button -->
        <div class="flex flex-col items-center justify-start w-40">
          <div
            @click="addSlot"
            class="w-36 h-44 bg-gray-800 border-2 border-dashed border-gray-600 rounded-xl flex flex-col items-center justify-center gap-2 cursor-pointer hover:border-green-500 hover:bg-gray-700 transition"
          >
            <span class="text-3xl text-gray-500">+</span>
            <span class="text-xs text-gray-500">Add player</span>
          </div>
        </div>

      </div>
    </div>

    <!-- Stats comparison table -->
    <div v-if="selectedPlayers.some(p => p !== null)" class="mt-6 overflow-x-auto">
      <table class="w-full min-w-max">
        <tbody>
          <tr v-for="stat in statRows" :key="stat.key" class="border-b border-gray-800">
            <!-- Stat label -->
            <td class="py-3 px-4 text-gray-400 text-sm w-28">{{ stat.label }}</td>

            <!-- Stat values for each player -->
            <td
              v-for="(player, index) in selectedPlayers"
              :key="index"
              class="py-3 px-4 text-center"
            >
              <div
                v-if="player"
                :class="generateStats(player)[stat.key] === getBestStat(stat.key) ? 'bg-green-600' : 'bg-red-700'"
                class="w-16 h-10 rounded-lg flex flex-col items-center justify-center mx-auto"
              >
                <span class="text-white font-black text-sm">{{ generateStats(player)[stat.key] }}</span>
                <span class="text-white text-xs opacity-70">{{ stat.key }}</span>
              </div>
            </td>
          </tr>

          <!-- Draft score row -->
          <tr>
            <td class="py-3 px-4 text-gray-400 text-sm">Draft Score</td>
            <td
              v-for="(player, index) in selectedPlayers"
              :key="index"
              class="py-3 px-4 text-center"
            >
              <div
                v-if="player"
                :class="player.draft_score === Math.max(...selectedPlayers.filter(p => p).map(p => p.draft_score)) ? 'bg-green-600' : 'bg-red-700'"
                class="w-16 h-10 rounded-lg flex flex-col items-center justify-center mx-auto"
              >
                <span class="text-white font-black text-sm">{{ player.draft_score }}</span>
                <span class="text-white text-xs opacity-70">SCR</span>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else class="text-center text-gray-400 mt-8">
      Click "+ Add player" to start comparing! ⚔️
    </div>
  </div>
</template>