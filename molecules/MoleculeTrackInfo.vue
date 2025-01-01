<template>
  <div class="flex flex-wrap items-center mx-8 lg:mx-24 max-w-120 md:max-w-150">
    <div v-if="bandName" class="body3 mb-2 w-full whitespace-nowrap text-ellipsis overflow-hidden">{{ bandName }}</div>
    <div class="body2 text-grey w-full whitespace-nowrap text-ellipsis overflow-hidden">{{ trackName }}</div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from '@nuxtjs/composition-api'

export default defineComponent({
  name: 'MoleculeTrackInfo',
  props: {
    bandName: {
      type: String,
      default: '',
    },
    trackName: {
      type: String,
      required: true,
    },
  },
})
</script>
