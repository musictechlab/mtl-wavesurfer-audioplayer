<template>
  <div class="flex flex-wrap border-1 border-black p-4 absolute bg-white bottom-60 z-50">
    <molecule-icon-button icon="share" @click="$emit('share')" />
    <molecule-icon-button icon="download" @click="$emit('download')" />
    <molecule-icon-button icon="loop" :class="isPlayingLoop && 'bg-light-grey'" @click="$emit('play-loop')" />
    <molecule-icon-button icon="close" @click="$emit('remove')" />
  </div>
</template>

<script lang="ts">
import MoleculeIconButton from '@/molecules/MoleculeIconButton.vue'
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'OrganismHookControls',
  components: { MoleculeIconButton },
  props: {
    isPlayingLoop: {
      type: Boolean,
      required: false,
    },
  },
  emits: ['share', 'download', 'play-loop', 'remove'],
})
</script>
