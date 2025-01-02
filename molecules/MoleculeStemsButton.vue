<template>
  <button
    :disabled="disabled"
    class="flex flex-wrap items-center justify-center h-30 cursor-pointer hover:opacity-80 transition-opacity w-30 md:w-auto"
    @click="$emit('click')"
  >
    <atom-icon name="stems" />
    <p class="hidden md:block body2 w-full font-bold">{{ stemsTitle }}</p>
  </button>
</template>

<script lang="ts">
import AtomIcon from '@/atoms/AtomIcon.vue'
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'MoleculeStemsButton',
  components: { AtomIcon },
  props: {
    disabled: {
      type: Boolean,
      default: false,
    },
    stemsTitle: {
      type: String,
      default: 'Stems',
    },
  },
  emits: ['click'],
})
</script>
