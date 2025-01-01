<template>
  <div ref="menuControl" class="relative md:hidden">
    <molecule-icon-button icon="menu" class="flex md:hidden" @click="isMenuVisible = !isMenuVisible" />

    <div
      v-if="isMenuVisible"
      class="absolute bottom-36 flex flex-wrap bg-white border-1 border-black p-8 right-0 z-50 w-78"
    >
      <molecule-icon-button :disabled="isPreviousDisabled" icon="previous" @click="$emit('previous')" />
      <molecule-icon-button :disabled="isNextDisabled" icon="next" @click="$emit('next')" />
      <molecule-icon-button :class="isShuffle && 'bg-light-grey'" icon="shuffle" @click="$emit('toggle-shuffle')" />
      <molecule-icon-button v-if="false" icon="hook" :disabled="hook" @click="$emit('add-hook')" />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from '@nuxtjs/composition-api'
import MoleculeIconButton from '@/molecules/MoleculeIconButton.vue'
import { useClickOutside } from '@/src/composables/click-outside.composable'

export default defineComponent({
  name: 'MoleculeMenu',
  components: { MoleculeIconButton },
  props: {
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
    hook: {
      type: Object,
      required: false,
      default: () => ({}),
    },
  },
  emits: ['previous', 'next', 'toggle-shuffle', 'add-hook'],
  setup() {
    const menuControl = ref(null)
    const isMenuVisible = ref(false)

    useClickOutside(menuControl, () => (isMenuVisible.value = false))

    return {
      menuControl,
      isMenuVisible,
    }
  },
})
</script>
