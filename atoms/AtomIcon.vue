<template>
  <component :is="icons[name]" />
</template>

<script lang="ts">
import icons from '@/assets/icons'
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'AtomIcon',
  props: {
    name: {
      type: String,
      required: true,
    },
  },
  setup() {
    return {
      icons,
    }
  },
})
</script>
