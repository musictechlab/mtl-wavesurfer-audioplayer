<template>
  <div ref="volumeControl" class="relative bg-white">
    <molecule-icon-button icon="volumeOff" @click="isVolumeBarVisible = !isVolumeBarVisible" />

    <div v-if="isVolumeBarVisible" class="absolute bottom-36 flex flex-col z-100 bg-white">
      <molecule-icon-button icon="volumeOn" class="mb-8" @click="$emit('volumeChange', 100)" />
      <div class="w-30 h-160 relative">
        <input
          class="-rotate-90 w-160 absolute appearance-none h-[15px] rounded-[15px] border-1 border-black overflow-hidden top-volume-top left-volume-left"
          type="range"
          :value="value"
          min="0"
          max="100"
          @change="onVolumeChange($event)"
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from '@nuxtjs/composition-api'
import MoleculeIconButton from '@/molecules/MoleculeIconButton.vue'
import { useClickOutside } from '@/src/composables/click-outside.composable'

export default defineComponent({
  name: 'MoleculeVolumeControl',
  components: { MoleculeIconButton },
  props: {
    value: {
      type: Number,
      required: true,
    },
  },
  emits: ['volumeChange', 'volume-change'],
  setup(props, { emit }) {
    const volumeControl = ref(null)
    const isVolumeBarVisible = ref(false)

    useClickOutside(volumeControl, () => (isVolumeBarVisible.value = false))

    const onVolumeChange = (event: Event) => {
      emit('volume-change', (event.target as HTMLInputElement).value)
    }

    return {
      volumeControl,
      isVolumeBarVisible,
      onVolumeChange,
    }
  },
})
</script>

<style>
input[type='range']::-webkit-slider-thumb {
  box-shadow:
    -120px 0 0 115px #000,
    inset 0 0 0 8px #000;
  @apply w-[13px] h-[13px] rounded-[13px] bg-black relative appearance-none;
}

input[type='range']::-webkit-slider-runnable-track {
  @apply h-[13px] w-160 rounded-[13px];
}

input[type='range']::-moz-range-thumb,
input[type='range']::-ms-thumb {
  @apply bg-black cursor-pointer;
}
</style>
