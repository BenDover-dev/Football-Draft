<!-- PlayerCard.vue -->
<!-- EA FC Mobile style player card component. -->
<!-- Stats are intelligently generated based on position and FPL performance data -->
<!-- PAC, SHO, PAS, DRI, DEF, PHY are weighted by position type -->
<!-- Card tier: Gold=OVR 80+, Silver=OVR 65-79, Bronze=below 65 -->

<script setup>
const props = defineProps({
  player: Object,
  onAdd: Function,
  onClick: Function,
})

// Scale a value between a min and max range
const scale = (value, min, max) => Math.min(Math.max(Math.round(value), min), max)

// Performance boost factor based on FPL data (0 to 1)
const getBoost = (player) => {
  const formBoost = Math.min(player.form / 15, 1)
  const pointsBoost = Math.min(player.total_points / 300, 1)
  const priceBoost = Math.min(player.price / 15, 1)
  return (formBoost * 0.4 + pointsBoost * 0.4 + priceBoost * 0.2)
}

// Generate realistic stats based on position and performance
const generateStats = (player) => {
  const boost = getBoost(player)
  const b = boost * 30  // max bonus from performance

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

// Calculate OVR from stats
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

// Card tier based on OVR
const getTier = (ovr) => {
  if (ovr >= 80) return 'gold'
  if (ovr >= 65) return 'silver'
  return 'bronze'
}

// Card gradient based on tier
const getTierGradient = (ovr) => {
  const tier = getTier(ovr)
  if (tier === 'gold') return 'linear-gradient(135deg, #c8a84b 0%, #f5e170 30%, #c8a84b 60%, #8b6914 100%)'
  if (tier === 'silver') return 'linear-gradient(135deg, #8a9bb0 0%, #c8d6e5 30%, #8a9bb0 60%, #4a5568 100%)'
  return 'linear-gradient(135deg, #8b5e3c 0%, #c49a6c 30%, #8b5e3c 60%, #4a2c0a 100%)'
}

// Text color based on tier
const getTierText = (ovr) => {
  const tier = getTier(ovr)
  if (tier === 'gold') return '#5a3e00'
  if (tier === 'silver') return '#2d3748'
  return '#3d1a00'
}

// Position color
const getPositionColor = (position) => {
  const colors = {
    GK: '#f6c90e',
    DEF: '#3b82f6',
    MID: '#22c55e',
    FWD: '#ef4444',
  }
  return colors[position] || '#6b7280'
}
</script>

<template>
  <div class="flex flex-col items-center gap-2">
    <!-- EA FC Style Card -->
    <div
      class="relative w-44 cursor-pointer hover:scale-105 transition-transform duration-200"
      style="clip-path: polygon(0 0, 85% 0, 100% 8%, 100% 100%, 0 100%)"
      :style="`background: ${getTierGradient(getOVR(generateStats(player), player.position))}`"
      @click="onClick && onClick(player)"
    >
      <!-- Top: OVR + Position -->
      <div class="absolute top-2 left-2 flex flex-col items-center">
        <span
          class="text-2xl font-black leading-none"
          :style="`color: ${getTierText(getOVR(generateStats(player), player.position))}`"
        >
          {{ getOVR(generateStats(player), player.position) }}
        </span>
        <span
          class="text-xs font-black mt-0.5"
          :style="`color: ${getPositionColor(player.position)}`"
        >
          {{ player.position }}
        </span>
      </div>

      <!-- Player photo -->
      <div class="flex justify-center pt-2 pb-1">
        <img
          :src="`https://resources.premierleague.com/premierleague/photos/players/110x140/p${player.photo}.png`"
          :alt="player.name"
          class="w-32 h-36 object-cover object-top"
          @error="$event.target.src='https://resources.premierleague.com/premierleague/photos/players/110x140/Photo-Missing.png'"
        />
      </div>

      <!-- Player name -->
      <div
        class="text-center text-xs font-black px-2 pb-1 truncate"
        :style="`color: ${getTierText(getOVR(generateStats(player), player.position))}`"
      >
        {{ player.name.split(' ').slice(-1)[0].toUpperCase() }}
      </div>

      <!-- Divider -->
      <div
        class="mx-3 mb-1"
        :style="`border-top: 1px solid ${getTierText(getOVR(generateStats(player), player.position))}40`"
      ></div>

      <!-- Stats grid -->
      <div class="grid grid-cols-3 gap-x-2 gap-y-0.5 px-3 pb-3">
        <div
          v-for="(value, label) in generateStats(player)"
          :key="label"
          class="flex gap-1 items-center"
        >
          <span
            class="text-xs font-black"
            :style="`color: ${getTierText(getOVR(generateStats(player), player.position))}`"
          >
            {{ value }}
          </span>
          <span
            class="text-xs opacity-70"
            :style="`color: ${getTierText(getOVR(generateStats(player), player.position))}`"
          >
            {{ label }}
          </span>
        </div>
      </div>
    </div>

    <!-- Add to Squad button -->
    <button
      @click="onAdd(player)"
      class="w-44 bg-green-600 hover:bg-green-500 text-white text-xs font-bold py-1.5 rounded-lg transition"
    >
      + Add to Squad
    </button>
  </div>
</template>