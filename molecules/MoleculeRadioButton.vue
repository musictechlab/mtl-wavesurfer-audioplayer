<template>
  <div
    class="border-1 border-black cursor-pointer w-20 h-20 relative rounded-2 flex justify-center items-center"
    @click="$emit('click')"
  >
    <div v-if="checked" class="w-10 h-10 bg-black rounded-2"></div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'MoleculeRadioButton',
  props: {
    checked: {
      type: Boolean,
      default: false,
    },
  },
  emits: ['click'],
})
</script>
