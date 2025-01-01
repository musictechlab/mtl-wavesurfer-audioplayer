<template>
  <div class="flex flex-wrap space-x-0 lg:space-x-8">
    <molecule-icon-button
      class="hidden md:flex"
      :disabled="isPreviousDisabled"
      icon="previous"
      @click="$emit('previous')"
    />
    <molecule-icon-button v-if="isPlaying" icon="pause" @click="$emit('toggle-play')" />
    <molecule-icon-button v-else icon="play" @click="$emit('toggle-play')" />
    <molecule-icon-button class="hidden md:flex" :disabled="isNextDisabled" icon="next" @click="$emit('next')" />
    <molecule-icon-button
      :class="[isShuffle && 'bg-light-grey', 'hidden md:flex']"
      icon="shuffle"
      @click="$emit('toggle-shuffle')"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent } from '@nuxtjs/composition-api'
import MoleculeIconButton from '@/molecules/MoleculeIconButton.vue'

export default defineComponent({
  name: 'OrganismAudioControls',
  components: { MoleculeIconButton },
  props: {
    isPlaying: {
      type: Boolean,
      required: false,
    },
    isPreviousDisabled: {
      type: Boolean,
      required: false,
    },
    isNextDisabled: {
      type: Boolean,
      required: false,
    },
    isShuffle: {
      type: Boolean,
      required: false,
    },
  },
  emits: ['previous', 'toggle-play', 'next', 'toggle-shuffle'],
})
</script>
