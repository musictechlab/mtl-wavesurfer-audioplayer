<template>
  <button
    :disabled="disabled"
    :class="[
      'flex items-center justify-center',
      small ? 'w-24 h-24' : 'w-30 h-30',
      disabled ? 'cursor-not-allowed' : 'cursor-pointer hover:opacity-80 transition-opacity',
    ]"
    @click="$emit('click')"
  >
    <slot v-if="$slots.icon" name="icon" />
    <atom-icon v-else-if="icon" :name="icon" />
  </button>
</template>

<script lang="ts">
import AtomIcon from '@/atoms/AtomIcon.vue'
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'MoleculeIconButton',
  components: { AtomIcon },
  props: {
    icon: {
      type: String,
      default: '',
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    small: {
      type: Boolean,
      default: false,
    },
  },
  emits: ['click'],
})
</script>
